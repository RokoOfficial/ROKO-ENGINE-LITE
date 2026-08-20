#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ROKO ROUTER — roko.py
================================================================================
O motor da linguagem ROKO Script v2: avaliador seguro de expressões (AST,
sem eval()/exec() nativo), parser de blocos (IF/ELSE/END, WHILE/END,
FOR/END, BREAK/CONTINUE) e o interpretador (RokoInterpreter).

Depende apenas de tools.py (para resolver instruções CALL via
execute_tool) — não sabe nada sobre HTTP, Quart, ou rotas. Isso permite
usar o motor isoladamente (embutido em outro programa Python, testes,
etc.) sem precisar subir a API.

Novidade desta versão: RokoInterpreter.execute() aceita um parâmetro
opcional `on_event`, chamado em tempo real a cada evento de execução
(SET, CALL, IF, laços, RETURN, erro...). É isso que api.py usa para
implementar o streaming SSE de /script/stream — sem esse hook, só seria
possível streamar o trace inteiro de uma vez, depois que o script já
tivesse terminado.

Também suporta despacho DINÂMICO de ferramenta: `CALL ${variavel} WITH
...` resolve o nome da ferramenta a partir de uma variável em tempo de
execução, em vez de exigir um nome literal fixo no texto do script. É o
que torna possível escrever um roteador semântico em ROKO Script puro
(ver ROKO_ROUTER.hmp): o script decide qual ferramenta chamar com base
em busca/pontuação, e só então executa essa decisão via CALL dinâmico.
================================================================================
"""
from __future__ import annotations

import ast
import re
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from tools import execute_tool

# ============================================================================
# LIMITES DE SEGURANÇA DO MOTOR
# ============================================================================
MAX_SCRIPT_LINES = 10000
MAX_WHILE_ITERATIONS = 5000
MAX_LOOP_TOTAL_STEPS = 50000   # teto global de passos de laço por execução (FOR+WHILE somados)
MAX_BLOCK_DEPTH = 64           # profundidade máxima de aninhamento IF/WHILE/FOR
MAX_EXEC_SECONDS = 15          # teto de tempo de execução de um script


class ExpressionError(Exception):
    """Erro de avaliação de expressão do ROKO Script."""


class SafeExpressionEvaluator:
    """
    Avalia expressões aritméticas, lógicas e de comparação usando a árvore
    sintática (ast) do Python, restrita a um conjunto seguro de nós.

    Isso resolve uma lacuna real do motor anterior: expressões como
    "1 + 2 * 3" ou "${a} + ${b} * 2" eram apenas documentadas, mas nunca
    avaliadas de fato (ast.literal_eval não executa operadores binários
    de forma genérica). Aqui elas são de fato calculadas.

    Nós permitidos: constantes, listas/tuplas/dicionários literais,
    operadores binários (+ - * / // % **), unários (- + not),
    comparações (== != < <= > >= in / not in), operadores booleanos
    (and / or), nomes de variáveis e acesso a índice/atributo simples
    (var[0], var.chave). Chamadas de função (Call) NUNCA são permitidas —
    chamar ferramentas é responsabilidade exclusiva do comando CALL.
    """

    _ALLOWED_NODES = (
        ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Compare,
        ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Name, ast.Load,
        ast.And, ast.Or, ast.Not, ast.UAdd, ast.USub,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn,
        ast.Subscript, ast.Index, ast.Slice, ast.Attribute,
    )

    def __init__(self, resolver: Callable[[str], Any]):
        """
        Args:
            resolver: função chamada para resolver o valor de um nome (Name)
                      que não seja True/False/None.
        """
        self._resolver = resolver

    def evaluate(self, expr: str) -> Any:
        expr = expr.strip()
        if expr == "":
            return None
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError as e:
            raise ExpressionError(f"Expressão inválida: '{expr}' ({e})") from e
        self._validate(tree)
        return self._eval(tree.body)

    def _validate(self, node: ast.AST) -> None:
        for child in ast.walk(node):
            if not isinstance(child, self._ALLOWED_NODES):
                raise ExpressionError(
                    f"Construção não permitida na expressão: {type(child).__name__}"
                )

    def _eval(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id == "true" or node.id == "True":
                return True
            if node.id == "false" or node.id == "False":
                return False
            if node.id in ("null", "none", "None"):
                return None
            return self._resolver(node.id)
        if isinstance(node, ast.List):
            return [self._eval(e) for e in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(self._eval(e) for e in node.elts)
        if isinstance(node, ast.Dict):
            return {self._eval(k): self._eval(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.UnaryOp):
            val = self._eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            if isinstance(node.op, ast.Not):
                return not val
            raise ExpressionError("Operador unário não suportado")
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            return self._apply_binop(node.op, left, right)
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                result = True
                for v in node.values:
                    result = self._eval(v)
                    if not result:
                        return result
                return result
            if isinstance(node.op, ast.Or):
                result = False
                for v in node.values:
                    result = self._eval(v)
                    if result:
                        return result
                return result
            raise ExpressionError("Operador lógico não suportado")
        if isinstance(node, ast.Compare):
            left = self._eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval(comparator)
                if not self._apply_compare(op, left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.Subscript):
            container = self._eval(node.value)
            key_node = node.slice
            if isinstance(key_node, ast.Index):  # Python < 3.9 compat
                key_node = key_node.value
            key = self._eval(key_node)
            try:
                return container[key]
            except (KeyError, IndexError, TypeError):
                return None
        if isinstance(node, ast.Attribute):
            base = self._eval(node.value)
            if isinstance(base, dict):
                return base.get(node.attr)
            return getattr(base, node.attr, None)
        raise ExpressionError(f"Nó não suportado: {type(node).__name__}")

    @staticmethod
    def _apply_binop(op: ast.AST, left: Any, right: Any) -> Any:
        try:
            if isinstance(op, ast.Add):
                return left + right
            if isinstance(op, ast.Sub):
                return left - right
            if isinstance(op, ast.Mult):
                return left * right
            if isinstance(op, ast.Div):
                return left / right
            if isinstance(op, ast.FloorDiv):
                return left // right
            if isinstance(op, ast.Mod):
                return left % right
            if isinstance(op, ast.Pow):
                return left ** right
        except ZeroDivisionError as e:
            raise ExpressionError("Divisão por zero na expressão") from e
        except TypeError as e:
            raise ExpressionError(f"Tipos incompatíveis na expressão: {e}") from e
        raise ExpressionError("Operador binário não suportado")

    @staticmethod
    def _apply_compare(op: ast.AST, left: Any, right: Any) -> bool:
        try:
            if isinstance(op, ast.Eq):
                return left == right
            if isinstance(op, ast.NotEq):
                return left != right
            if isinstance(op, ast.Lt):
                return left < right
            if isinstance(op, ast.LtE):
                return left <= right
            if isinstance(op, ast.Gt):
                return left > right
            if isinstance(op, ast.GtE):
                return left >= right
            if isinstance(op, ast.In):
                return left in right
            if isinstance(op, ast.NotIn):
                return left not in right
        except TypeError as e:
            raise ExpressionError(f"Comparação inválida entre tipos: {e}") from e
        raise ExpressionError("Operador de comparação não suportado")


# ============================================================================
# CONTROLE DE FLUXO INTERNO (sinais de execução)
# ============================================================================

class _BreakSignal(Exception):
    """Sinal interno para BREAK dentro de um laço."""


class _ContinueSignal(Exception):
    """Sinal interno para CONTINUE dentro de um laço."""


class _ReturnSignal(Exception):
    """Sinal interno para RETURN."""


# ============================================================================
# ANALISADOR DE BLOCOS — transforma linhas soltas em uma árvore real
# IF/ELSE/END, WHILE/END, FOR/END são de fato pareados e aninháveis.
# ============================================================================

class RokoBlockParser:
    """
    Agrupa as linhas do script em uma árvore de blocos.

    O motor anterior tratava IF/FOR/WHILE como comandos de uma única linha
    (`IF cond THEN comando`), sem suporte real a END — múltiplos comandos
    dentro de um laço ou condicional eram impossíveis. Este parser resolve
    isso: quando a linha termina em THEN/DO (sem comando na mesma linha),
    um bloco é aberto e só se fecha em uma linha END correspondente,
    permitindo qualquer número de instruções, aninhamento e ELSE.

    A forma de uma linha só (`IF cond THEN comando`) continua funcionando
    para compatibilidade retroativa, sem exigir END.
    """

    def __init__(self):
        self.errors: List[str] = []

    def parse(self, script: str) -> List[Dict[str, Any]]:
        raw_lines = str(script).splitlines()
        if len(raw_lines) > MAX_SCRIPT_LINES:
            raise ExpressionError(f"Script excede o limite de {MAX_SCRIPT_LINES} linhas")

        # Remove comentários e linhas vazias, preservando o número da linha original
        lines: List[Tuple[int, str]] = []
        for i, raw in enumerate(raw_lines, 1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("#"):
                continue
            lines.append((i, stripped))

        pos = 0

        def parse_block(terminators: Tuple[str, ...], depth: int) -> Tuple[List[Dict[str, Any]], Optional[str]]:
            nonlocal pos
            if depth > MAX_BLOCK_DEPTH:
                raise ExpressionError("Profundidade máxima de blocos excedida (aninhamento demais)")
            stmts: List[Dict[str, Any]] = []
            closing = None
            while pos < len(lines):
                line_num, line = lines[pos]
                upper = line.upper()

                # Palavra-chave de fechamento/transição (END, ELSE)
                first_word = upper.split(None, 1)[0] if upper else ""
                if first_word in terminators:
                    closing = first_word
                    pos += 1
                    return stmts, closing
                if first_word in ("END", "ELSE") and first_word not in terminators:
                    raise ExpressionError(
                        f"'{first_word}' inesperado na linha {line_num} (nenhum bloco IF/WHILE/FOR aberto aqui)"
                    )

                m = re.match(r"IF\s+(.+?)\s+THEN\s*(.*)$", line, re.I)
                if m:
                    condition, inline_cmd = m.groups()
                    pos += 1
                    if inline_cmd.strip():
                        # Forma de uma linha: sem END, sem ELSE
                        then_body = [{"type": "line", "line_num": line_num, "text": inline_cmd.strip()}]
                        stmts.append({"type": "if", "line_num": line_num, "condition": condition,
                                      "then": then_body, "else": []})
                    else:
                        then_body, term = parse_block(("ELSE", "END"), depth + 1)
                        else_body: List[Dict[str, Any]] = []
                        if term == "ELSE":
                            else_body, _term2 = parse_block(("END",), depth + 1)
                        elif term is None:
                            raise ExpressionError(f"IF aberto na linha {line_num} sem END correspondente")
                        stmts.append({"type": "if", "line_num": line_num, "condition": condition,
                                      "then": then_body, "else": else_body})
                    continue

                m = re.match(r"WHILE\s+(.+?)\s+DO\s*(.*)$", line, re.I)
                if m:
                    condition, inline_cmd = m.groups()
                    pos += 1
                    if inline_cmd.strip():
                        body = [{"type": "line", "line_num": line_num, "text": inline_cmd.strip()}]
                    else:
                        body, term = parse_block(("END",), depth + 1)
                        if term is None:
                            raise ExpressionError(f"WHILE aberto na linha {line_num} sem END correspondente")
                    stmts.append({"type": "while", "line_num": line_num, "condition": condition, "body": body})
                    continue

                m = re.match(r"FOR\s+([A-Za-z_]\w*)\s+IN\s+(.+?)\s+DO\s*(.*)$", line, re.I)
                if m:
                    var_name, items_expr, inline_cmd = m.groups()
                    pos += 1
                    if inline_cmd.strip():
                        body = [{"type": "line", "line_num": line_num, "text": inline_cmd.strip()}]
                    else:
                        body, term = parse_block(("END",), depth + 1)
                        if term is None:
                            raise ExpressionError(f"FOR aberto na linha {line_num} sem END correspondente")
                    stmts.append({"type": "for", "line_num": line_num, "var": var_name,
                                  "items_expr": items_expr, "body": body})
                    continue

                # Linha simples (SET, CALL, RETURN, BREAK, CONTINUE, expressão, atribuição)
                stmts.append({"type": "line", "line_num": line_num, "text": line})
                pos += 1

            return stmts, closing

        body, _ = parse_block((), 0)
        if pos < len(lines):
            # Sobraram tokens de fechamento sem abertura correspondente (ex.: END solto)
            line_num, line = lines[pos]
            raise ExpressionError(f"'{line.split()[0]}' inesperado na linha {line_num} (sem bloco aberto)")
        return body


# ============================================================================
# INTERPRETADOR ROKO SCRIPT
# ============================================================================

class RokoInterpreter:
    """
    Interpretador para a linguagem ROKO Script (motor v2).

    Suporta:
    - Variáveis: SET nome TO valor  |  nome = valor
    - Chamada de ferramentas: CALL tool WITH param=valor, ... [AS var]
    - Retorno: RETURN expressão
    - Condicionais em bloco: IF condição THEN ... [ELSE ...] END
      (a forma de uma linha "IF cond THEN comando" continua válida)
    - Laços em bloco: FOR item IN lista DO ... END
    - Laços em bloco: WHILE condição DO ... END
    - BREAK / CONTINUE dentro de laços
    - Comentários: // comentário  ou  # comentário
    - Interpolação de texto: ${variavel}
    - Expressões reais (aritméticas, lógicas, comparações): 1 + 2 * 3,
      ${a} >= ${b} AND ${c} != null, etc. — avaliadas por AST seguro,
      não apenas reconhecidas por regex.

    A saída (`output`) é uma lista de strings legíveis para humanos,
    mantida por compatibilidade. `trace` é a saída estruturada nova:
    uma lista de eventos com linha, profundidade de aninhamento, tipo
    de instrução e detalhe — pensada para depuração e para consumo por
    outras ferramentas (dashboards, HGR, etc).
    """

    # Expressão regular para interpolação
    INTERPOLATION_RE = re.compile(r"\$\{([^}]+)\}")

    def __init__(self):
        """Inicializa o interpretador."""
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []
        self.trace: List[Dict[str, Any]] = []
        self.last_result: Dict[str, Any] = {}
        self._returned = False
        self._debug = False
        self._loop_steps = 0
        self._evaluator = SafeExpressionEvaluator(self._resolve_path)
        self._start_time = 0.0
        self._on_event: Optional[Callable[[Dict[str, Any]], None]] = None

    def _trace_add(self, event: Dict[str, Any]) -> None:
        """
        Acrescenta um evento ao trace e, se um `on_event` foi passado para
        execute(), o notifica IMEDIATAMENTE (antes de seguir para a próxima
        instrução) — é o gancho que permite streaming em tempo real (SSE)
        em vez de só poder entregar o trace inteiro no final.
        """
        self.trace.append(event)
        if self._on_event is not None:
            self._on_event(event)

    def execute(self, script: str, variables: Optional[Dict[str, Any]] = None,
                debug: bool = False, on_event: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        """
        Executa um script ROKO.

        Args:
            script: Código fonte do script
            variables: Variáveis iniciais
            debug: Ativa modo debug
            on_event: Callback opcional, chamado a cada evento de execução
                (mesmo formato de cada item de `trace`) NO MOMENTO em que
                acontece, não só no final. Use para streaming (ex.: SSE em
                api.py). Deve ser rápido e não bloquear — é chamado de
                dentro do laço de execução do script.

        Returns:
            Dict[str, Any]: Resultado da execução, incluindo saída
            estruturada (`trace`) e estatísticas (`stats`).
        """
        self.variables = dict(variables or {})
        self.output = []
        self.trace = []
        self.last_result = {}
        self._returned = False
        self._debug = debug
        self._loop_steps = 0
        self._on_event = on_event
        self._start_time = time.monotonic()

        try:
            block = RokoBlockParser().parse(script)
        except ExpressionError as e:
            return self._fail(str(e), line_num=None)

        try:
            self._exec_block(block, depth=0)
        except _ReturnSignal:
            pass
        except (_BreakSignal, _ContinueSignal):
            return self._fail("BREAK/CONTINUE usado fora de um laço", line_num=None)
        except ExpressionError as e:
            return self._fail(str(e), line_num=getattr(e, "line_num", None))
        except Exception as e:
            if self._debug:
                import traceback
                traceback.print_exc()
            return self._fail(str(e), line_num=None)

        return {
            "success": True,
            "output": self.output,
            "trace": self.trace,
            "variables": self.variables,
            "return_value": self.last_result.get("default"),
            "last_result": self.last_result,
            "stats": self._stats(),
        }

    def _fail(self, message: str, line_num: Optional[int]) -> Dict[str, Any]:
        prefix = f"Erro na linha {line_num}: " if line_num else "Erro: "
        error_msg = f"{prefix}{message}"
        self.output.append(f"[ERRO] {error_msg}")
        self._trace_add({"event": "error", "line": line_num, "message": message})
        return {
            "success": False,
            "error": error_msg,
            "output": self.output,
            "trace": self.trace,
            "variables": self.variables,
            "last_result": self.last_result,
            "stats": self._stats(),
        }

    def _stats(self) -> Dict[str, Any]:
        return {
            "elapsed_ms": round((time.monotonic() - self._start_time) * 1000, 3),
            "statements_executed": sum(1 for t in self.trace if t.get("event") == "exec"),
            "tool_calls": sum(1 for t in self.trace if t.get("event") == "call"),
            "loop_steps": self._loop_steps,
        }

    def _check_time(self) -> None:
        if time.monotonic() - self._start_time > MAX_EXEC_SECONDS:
            raise ExpressionError(f"Script excedeu o tempo máximo de execução ({MAX_EXEC_SECONDS}s)")

    # ------------------------------------------------------------------------
    # EXECUÇÃO DA ÁRVORE DE BLOCOS
    # ------------------------------------------------------------------------

    def _exec_block(self, statements: List[Dict[str, Any]], depth: int) -> None:
        for stmt in statements:
            self._check_time()
            if stmt["type"] == "line":
                self._trace_and_process(stmt["line_num"], stmt["text"], depth)
            elif stmt["type"] == "if":
                self._exec_if(stmt, depth)
            elif stmt["type"] == "while":
                self._exec_while(stmt, depth)
            elif stmt["type"] == "for":
                self._exec_for(stmt, depth)
            else:
                raise ExpressionError(f"Instrução desconhecida: {stmt['type']}")

    def _trace_and_process(self, line_num: int, text: str, depth: int) -> None:
        upper = text.upper().strip()
        if upper == "BREAK":
            self._trace_add({"event": "exec", "line": line_num, "depth": depth, "type": "break"})
            raise _BreakSignal()
        if upper == "CONTINUE":
            self._trace_add({"event": "exec", "line": line_num, "depth": depth, "type": "continue"})
            raise _ContinueSignal()
        try:
            self._process_line(text, line_num=line_num, depth=depth)
        except (_BreakSignal, _ContinueSignal, _ReturnSignal):
            raise
        except ExpressionError:
            raise
        except Exception as e:
            raise ExpressionError(str(e)) from e

    def _exec_if(self, stmt: Dict[str, Any], depth: int) -> None:
        condition_true = self._eval_condition(stmt["condition"])
        self._trace_add({
            "event": "exec", "line": stmt["line_num"], "depth": depth, "type": "if",
            "condition": stmt["condition"], "result": condition_true,
        })
        if condition_true:
            self._exec_block(stmt["then"], depth + 1)
        elif stmt["else"]:
            self._exec_block(stmt["else"], depth + 1)

    def _exec_while(self, stmt: Dict[str, Any], depth: int) -> None:
        count = 0
        self._trace_add({"event": "exec", "line": stmt["line_num"], "depth": depth,
                            "type": "while_start", "condition": stmt["condition"]})
        while self._eval_condition(stmt["condition"]):
            count += 1
            self._loop_steps += 1
            if count > MAX_WHILE_ITERATIONS:
                raise ExpressionError(
                    f"WHILE na linha {stmt['line_num']} excedeu o limite de {MAX_WHILE_ITERATIONS} iterações"
                )
            if self._loop_steps > MAX_LOOP_TOTAL_STEPS:
                raise ExpressionError(f"Script excedeu o limite global de {MAX_LOOP_TOTAL_STEPS} passos de laço")
            self._check_time()
            try:
                self._exec_block(stmt["body"], depth + 1)
            except _BreakSignal:
                break
            except _ContinueSignal:
                continue
        self._trace_add({"event": "exec", "line": stmt["line_num"], "depth": depth,
                            "type": "while_end", "iterations": count})

    def _exec_for(self, stmt: Dict[str, Any], depth: int) -> None:
        items = self._evaluate_set_expression(stmt["items_expr"])
        if not isinstance(items, (list, tuple)):
            raise ExpressionError(f"FOR na linha {stmt['line_num']} requer uma lista ou tupla, recebeu {type(items).__name__}")
        self._trace_add({"event": "exec", "line": stmt["line_num"], "depth": depth,
                            "type": "for_start", "var": stmt["var"], "length": len(items)})
        count = 0
        for item in items:
            self.variables[stmt["var"]] = item
            self._loop_steps += 1
            count += 1
            if self._loop_steps > MAX_LOOP_TOTAL_STEPS:
                raise ExpressionError(f"Script excedeu o limite global de {MAX_LOOP_TOTAL_STEPS} passos de laço")
            self._check_time()
            try:
                self._exec_block(stmt["body"], depth + 1)
            except _BreakSignal:
                break
            except _ContinueSignal:
                continue
        self._trace_add({"event": "exec", "line": stmt["line_num"], "depth": depth,
                            "type": "for_end", "iterations": count})

    # ------------------------------------------------------------------------
    # MÉTODOS DE PARSING DE VALORES/PARÂMETROS
    # ------------------------------------------------------------------------

    @staticmethod
    def _split_top_level(text: str, separator: str = ",") -> List[str]:
        """
        Divide uma string respeitando parênteses, colchetes e aspas.

        Args:
            text: Texto a ser dividido
            separator: Separador

        Returns:
            List[str]: Partes divididas
        """
        parts = []
        start = 0
        depth = 0
        quote = None
        escaped = False

        for i, char in enumerate(text):
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue

            if char in ('"', "'"):
                quote = char
            elif char in "[{(":
                depth += 1
            elif char in "]})":
                depth = max(0, depth - 1)
            elif char == separator and depth == 0:
                parts.append(text[start:i].strip())
                start = i + 1

        parts.append(text[start:].strip())
        return [p for p in parts if p]

    @staticmethod
    def _strip_outer_quotes(value: str) -> Optional[str]:
        """
        Remove aspas externas se presentes.

        Args:
            value: String a ser processada

        Returns:
            Optional[str]: String sem aspas ou None se não houver aspas
        """
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            return value[1:-1]
        return None

    # ------------------------------------------------------------------------
    # MÉTODOS DE RESOLUÇÃO DE VALORES
    # ------------------------------------------------------------------------

    def _resolve_path(self, path: str) -> Any:
        """
        Resolve um caminho de variável ou resultado.

        Args:
            path: Caminho no formato "var" ou "var.sub" ou "last.tool"

        Returns:
            Any: Valor resolvido ou None
        """
        path = path.strip()

        # Acesso a resultados anteriores
        if path.startswith("last."):
            current = self.last_result
            parts = path[5:].split(".")
        else:
            first, *rest = path.split(".")

            if first in self.variables:
                current = self.variables[first]
                parts = rest
            elif path in self.last_result:
                return self.last_result[path]
            elif first in self.last_result and not rest:
                return self.last_result[first]
            else:
                # Tenta buscar diretamente em last_result
                if path in self.last_result:
                    return self.last_result[path]
                return None

        # Navega pelo caminho
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return None
            else:
                return None

        return current

    def _interpolate(self, text: str) -> str:
        """
        Interpola variáveis em um texto.

        Args:
            text: Texto com placeholders ${var}

        Returns:
            str: Texto interpolado
        """
        def repl(match: re.Match[str]) -> str:
            value = self._resolve_path(match.group(1))
            if value is None:
                return "None"
            return str(value)

        return self.INTERPOLATION_RE.sub(repl, str(text))

    def _evaluate_literal(self, expr: str) -> Any:
        """
        Avalia uma expressão de valor: literais, variáveis, aritmética,
        comparações e listas/dicionários — de fato calculados via
        SafeExpressionEvaluator (não apenas reconhecidos por regex).

        Ordem de resolução:
        1. String entre aspas -> interpola ${...} dentro dela e retorna string.
        2. Contém ${...} fora de aspas (ex.: "${a} + ${b} * 2") -> cada
           ${caminho} é substituído pelo valor Python real (preservando
           tipo — número continua número) e o resultado é avaliado como
           expressão. Isso corrige o bug do motor anterior, em que
           ${a} >= ${b} comparava strings em vez dos valores originais.
        3. Expressão "crua" (sem ${}) -> avaliada diretamente pelo
           SafeExpressionEvaluator, que resolve nomes de variável (a, b.x,
           lista[0]) e calcula operadores (+ - * / // % ** and or not
           == != < <= > >= in).
        4. Se nada disso for uma expressão válida, é tratada como texto
           literal com interpolação ${...} aplicada (comportamento antigo,
           mantido para strings soltas sem aspas).

        Args:
            expr: Expressão a ser avaliada

        Returns:
            Any: Valor da expressão
        """
        expr = expr.strip()

        # Strings com aspas: interpola o conteúdo e retorna como string
        quoted = self._strip_outer_quotes(expr)
        if quoted is not None:
            return self._interpolate(quoted)

        # Interpolação ${...} preservando tipo, fora de string entre aspas
        if "${" in expr:
            substituted = self._substitute_preserving_type(expr)
            if substituted != expr:
                try:
                    return self._evaluator.evaluate(substituted)
                except ExpressionError:
                    pass
                # Se não for uma expressão válida (ex.: texto solto com
                # placeholders no meio), retorna a versão interpolada como texto
                return self._interpolate(expr)

        # Palavra "solta" que não é uma expressão nem uma variável conhecida
        # (ex.: texto sem aspas) -> trata como literal de texto, como antes.
        if re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*|\.\d+)*", expr):
            if not self._path_is_known(expr):
                return expr

        # Expressão direta (aritmética, comparação, variável, lista, dict, literal)
        try:
            return self._evaluator.evaluate(expr)
        except ExpressionError:
            pass

        # Último recurso: texto literal com interpolação
        return self._interpolate(expr)

    def _path_is_known(self, path: str) -> bool:
        """Indica se um caminho de variável (a, a.b, last.x) resolve a algo definido."""
        first = path.split(".", 1)[0]
        if path.startswith("last."):
            return True
        return first in self.variables or path in self.last_result or first in self.last_result

    def _substitute_preserving_type(self, text: str) -> str:
        """
        Substitui cada ${caminho} pelo valor Python resolvido, escolhendo a
        forma certa conforme o contexto sintático ao redor de cada ocorrência:

        - ${caminho} em posição "crua" (fora de qualquer string entre aspas
          dentro do texto, ex.: dentro de um dict/lista literal como valor
          direto) -> substitui por `repr(valor)`, preservando o tipo, para
          que a expressão resultante calcule certo (números continuam
          números, listas continuam listas).
        - ${caminho} DENTRO de uma sub-string já entre aspas (ex.:
          "Bearer ${token}" usado como valor de um campo de um dict) ->
          substitui pelo texto puro do valor (str(valor), com aspas e
          barras invertidas escapadas), igual à interpolação normal — usar
          repr() aqui quebraria a string (ex.: geraria literalmente
          `Bearer ''` em vez de `Bearer ` para um token vazio).

        Corrige um bug real do motor: antes, QUALQUER ${...} no texto era
        sempre trocado por repr(), mesmo dentro de sub-strings — o que
        corrompia silenciosamente qualquer header/valor construído como
        "prefixo ${variavel} sufixo" dentro de um dict/lista.
        """
        result = []
        i = 0
        n = len(text)
        in_quote: Optional[str] = None
        while i < n:
            ch = text[i]

            if in_quote:
                if ch == "\\" and i + 1 < n:
                    result.append(text[i:i + 2])
                    i += 2
                    continue
                if ch == "$" and i + 1 < n and text[i + 1] == "{":
                    end = text.find("}", i + 2)
                    if end != -1:
                        path = text[i + 2:end]
                        value = self._resolve_path(path)
                        as_text = "" if value is None else (value if isinstance(value, str) else str(value))
                        escaped = as_text.replace("\\", "\\\\").replace(in_quote, "\\" + in_quote)
                        result.append(escaped)
                        i = end + 1
                        continue
                if ch == in_quote:
                    in_quote = None
                result.append(ch)
                i += 1
                continue

            if ch in ("'", '"'):
                in_quote = ch
                result.append(ch)
                i += 1
                continue

            if ch == "$" and i + 1 < n and text[i + 1] == "{":
                end = text.find("}", i + 2)
                if end != -1:
                    path = text[i + 2:end]
                    value = self._resolve_path(path)
                    result.append(repr(value))
                    i = end + 1
                    continue

            result.append(ch)
            i += 1

        return "".join(result)

    # ------------------------------------------------------------------------
    # MÉTODOS DE AVALIAÇÃO DE CONDIÇÕES
    # ------------------------------------------------------------------------

    def _eval_condition(self, expr: str) -> bool:
        """
        Avalia uma condição booleana real, com precedência correta
        (NOT > comparação > AND > OR) via SafeExpressionEvaluator.
        Aceita tanto os operadores em texto (AND/OR/NOT) quanto os
        símbolos Python (and/or/not) — normaliza antes de avaliar.

        Args:
            expr: Expressão condicional

        Returns:
            bool: Resultado da condição
        """
        expr = expr.strip()
        # Normaliza palavras-chave lógicas maiúsculas para o formato Python,
        # preservando o conteúdo de strings entre aspas.
        normalized = self._normalize_logical_keywords(expr)
        try:
            value = self._evaluator.evaluate(normalized)
        except ExpressionError:
            # Fallback: trata como literal/valor de variável isolado
            value = self._evaluate_literal(expr)
        return bool(value)

    @staticmethod
    def _normalize_logical_keywords(expr: str) -> str:
        """Converte AND/OR/NOT (qualquer caixa) para and/or/not fora de strings."""
        out = []
        i = 0
        in_quote = None
        n = len(expr)
        while i < n:
            ch = expr[i]
            if in_quote:
                out.append(ch)
                if ch == in_quote:
                    in_quote = None
                i += 1
                continue
            if ch in ("'", '"'):
                in_quote = ch
                out.append(ch)
                i += 1
                continue
            matched = False
            for kw, repl in (("AND", "and"), ("OR", "or"), ("NOT", "not"),
                              ("TRUE", "True"), ("FALSE", "False"),
                              ("NULL", "None"), ("NONE", "None")):
                kw_len = len(kw)
                if expr[i:i + kw_len].upper() == kw:
                    before_ok = i == 0 or not (expr[i - 1].isalnum() or expr[i - 1] == "_")
                    after_ok = i + kw_len >= n or not (expr[i + kw_len].isalnum() or expr[i + kw_len] == "_")
                    if before_ok and after_ok:
                        out.append(repl)
                        i += kw_len
                        matched = True
                        break
            if not matched:
                out.append(ch)
                i += 1
        return "".join(out)

    # ------------------------------------------------------------------------
    # PROCESSAMENTO DE LINHAS (instruções que não abrem blocos)
    # ------------------------------------------------------------------------

    def _process_line(self, line: str, line_num: Optional[int] = None, depth: int = 0) -> None:
        """
        Processa uma única linha "de folha" do script (não IF/WHILE/FOR,
        que já são resolvidos pela árvore de blocos antes de chegar aqui).

        Args:
            line: Linha do script
        """
        line = line.strip()

        # SET nome TO valor
        match = re.match(r"SET\s+([A-Za-z_]\w*)\s+TO\s+(.+)$", line, re.I)
        if match:
            name, expr = match.groups()
            value = self._evaluate_set_expression(expr)
            self.variables[name] = value
            self.output.append(f"SET {name} = {self._format_value(value)}")
            self._trace_add({"event": "exec", "line": line_num, "depth": depth,
                                "type": "set", "name": name, "value": value})
            return

        # Atribuição nome = valor (não confundir com == dentro de expressões)
        match = re.match(r"([A-Za-z_]\w*)\s*=(?!=)\s*(.+)$", line)
        if match:
            name, expr = match.groups()
            value = self._evaluate_set_expression(expr)
            self.variables[name] = value
            self.output.append(f"{name} = {self._format_value(value)}")
            self._trace_add({"event": "exec", "line": line_num, "depth": depth,
                                "type": "assign", "name": name, "value": value})
            return

        # CALL tool WITH params [AS var]  (nome literal OU dinâmico via ${var})
        match = re.match(r"CALL\s+([\w.]+|\$\{[^}]+\})\s+WITH\s+(.+?)(?:\s+AS\s+([A-Za-z_]\w*))?$", line, re.I)
        if match:
            tool_name, params_str, target = match.groups()
            value = self._do_call(tool_name, params_str, line_num, depth)
            if target:
                self.variables[target] = value
                self.output.append(f"SET {target} = {self._format_value(value)}")
            return

        # CALL tool (sem parâmetros) [AS var]  (nome literal OU dinâmico via ${var})
        match = re.match(r"CALL\s+([\w.]+|\$\{[^}]+\})\s*(?:\s+AS\s+([A-Za-z_]\w*))?$", line, re.I)
        if match:
            tool_name, target = match.groups()
            value = self._do_call(tool_name, "", line_num, depth)
            if target:
                self.variables[target] = value
                self.output.append(f"SET {target} = {self._format_value(value)}")
            return

        # RETURN expressão
        match = re.match(r"RETURN\s*(.*)$", line, re.I)
        if match and (match.group(1).strip() or line.strip().upper() == "RETURN"):
            expr = match.group(1).strip()
            value = self._evaluate_set_expression(expr) if expr else None
            self.last_result["default"] = value
            self.output.append(f"RETURN: {self._format_value(value)}")
            self._trace_add({"event": "exec", "line": line_num, "depth": depth,
                                "type": "return", "value": value})
            self._returned = True
            raise _ReturnSignal()

        # Expressão simples (avaliada e guardada como último resultado)
        value = self._evaluate_set_expression(line)
        self.last_result["default"] = value
        self.output.append(f"-> {self._format_value(value)}")
        self._trace_add({"event": "exec", "line": line_num, "depth": depth,
                            "type": "expr", "value": value})

    def _resolve_tool_name(self, token: str) -> str:
        """
        Resolve o nome de uma ferramenta em uma instrução CALL. Aceita duas
        formas:
        - Literal: `math.sum` — usado como está.
        - Dinâmico: `${variavel}` — resolve o valor da variável em tempo de
          execução e usa como nome da ferramenta. Isso é o que permite um
          "router" escrito em ROKO Script decidir EM TEMPO DE EXECUÇÃO qual
          ferramenta chamar (ex.: `CALL ${melhor_tool} WITH ...`), em vez de
          o nome da ferramenta ter que estar fixo no texto do script.

        Raises:
            ExpressionError: se a forma dinâmica não resolver para uma string.
        """
        token = token.strip()
        if token.startswith("${") and token.endswith("}"):
            path = token[2:-1]
            value = self._resolve_path(path)
            if not isinstance(value, str) or not value:
                raise ExpressionError(
                    f"Nome de ferramenta dinâmico '{token}' não resolveu para uma string "
                    f"não vazia (obteve {value!r})"
                )
            return value
        return token

    def _do_call(self, tool_name: str, params_str: str, line_num: Optional[int], depth: int) -> Any:
        resolved_name = self._resolve_tool_name(tool_name)
        params = self._parse_params(params_str) if params_str.strip() else {}
        result = execute_tool(resolved_name, params)

        if not result["success"]:
            raise ExpressionError(f"CALL {resolved_name} falhou: {result['error']}")

        value = result["result"]
        self.last_result[resolved_name] = value
        self.last_result["default"] = value
        self.output.append(f"[CALL] {resolved_name} -> {self._format_value(value)}")
        self._trace_add({"event": "call", "line": line_num, "depth": depth,
                            "tool": resolved_name, "tool_expr": tool_name, "params": params, "result": value})
        return value

    def _evaluate_set_expression(self, expr: str) -> Any:
        """
        Avalia uma expressão para atribuição/retorno/parâmetro. Suporta a
        forma inline `CALL tool WITH params` dentro de uma expressão
        (nome literal ou dinâmico via ${var}), e delega o restante para o
        avaliador seguro de expressões (aritmética, comparações,
        interpolação de ${var}).

        Args:
            expr: Expressão a ser avaliada

        Returns:
            Any: Valor da expressão
        """
        expr = expr.strip()

        # CALL tool WITH params (forma inline, nome literal ou dinâmico)
        call_match = re.match(r"CALL\s+([\w.]+|\$\{[^}]+\})\s+WITH\s+(.+)$", expr, re.I)
        if call_match:
            tool_name, params_str = call_match.groups()
            return self._do_call(tool_name, params_str, None, 0)

        call_match = re.match(r"CALL\s+([\w.]+|\$\{[^}]+\})\s*$", expr, re.I)
        if call_match:
            return self._do_call(call_match.group(1), "", None, 0)

        return self._evaluate_literal(expr)

    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """
        Parseia parâmetros de uma chamada de ferramenta.

        Args:
            params_str: String com parâmetros no formato "key=value, key2=value2"
                — ou, na forma abreviada, uma única referência a variável
                dict: "${params}". Nesse caso o dict inteiro é usado como
                os parâmetros da chamada (equivalente a "spread"/**kwargs),
                em vez de precisar listar cada chave manualmente. É isso
                que permite um router escrito em ROKO Script montar os
                parâmetros dinamicamente (ex.: a partir de uma busca ou de
                uma entrada externa) e repassá-los para `CALL ${tool} WITH
                ${params}`, sem precisar saber os nomes das chaves em
                tempo de escrita do script.

        Returns:
            Dict[str, Any]: Dicionário de parâmetros
        """
        stripped = params_str.strip()
        spread_match = re.fullmatch(r"\$\{([^}]+)\}", stripped)
        if spread_match:
            value = self._resolve_path(spread_match.group(1))
            if not isinstance(value, dict):
                raise ExpressionError(
                    f"CALL ... WITH {stripped} exige uma variável do tipo dict "
                    f"(obteve {type(value).__name__})"
                )
            return dict(value)

        params = {}
        for part in self._split_top_level(params_str):
            if "=" not in part:
                raise ValueError(f"Parâmetro inválido: '{part}'")

            key, raw_value = part.split("=", 1)
            params[key.strip()] = self._evaluate_set_expression(raw_value.strip())

        return params

    @staticmethod
    def _format_value(value: Any) -> str:
        """
        Formata um valor para exibição.

        Args:
            value: Valor a ser formatado

        Returns:
            str: Valor formatado
        """
        if isinstance(value, str):
            return f'"{value}"'
        if isinstance(value, list):
            return f"[{', '.join(RokoInterpreter._format_value(v) for v in value[:10])}{'...' if len(value) > 10 else ''}]"
        if isinstance(value, dict):
            items = list(value.items())[:10]
            formatted = ", ".join(f"{k}: {RokoInterpreter._format_value(v)}" for k, v in items)
            return f"{{{formatted}{'...' if len(value) > 10 else ''}}}"
        return str(value)
