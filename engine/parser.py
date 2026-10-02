#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinais de controle de fluxo e parser de blocos do ROKO Script.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from .limits import MAX_BLOCK_DEPTH, MAX_SCRIPT_LINES

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
