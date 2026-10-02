#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avaliador seguro de expressões do ROKO Script (AST restrita).
"""
from __future__ import annotations

import ast
from typing import Any, Callable

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
