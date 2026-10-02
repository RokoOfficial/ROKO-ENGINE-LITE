"""
ROKO ENGINE — motor modular da linguagem ROKO Script.

Exporta as classes principais usadas pela fachada (APP/router) e por testes.
"""

from .limits import (
    MAX_SCRIPT_LINES,
    MAX_WHILE_ITERATIONS,
    MAX_LOOP_TOTAL_STEPS,
    MAX_BLOCK_DEPTH,
    MAX_EXEC_SECONDS,
)
from .expression import ExpressionError, SafeExpressionEvaluator
from .parser import RokoBlockParser
from .interpreter import RokoInterpreter, _BreakSignal, _ContinueSignal, _ReturnSignal

__all__ = [
    "MAX_SCRIPT_LINES",
    "MAX_WHILE_ITERATIONS",
    "MAX_LOOP_TOTAL_STEPS",
    "MAX_BLOCK_DEPTH",
    "MAX_EXEC_SECONDS",
    "ExpressionError",
    "SafeExpressionEvaluator",
    "RokoBlockParser",
    "RokoInterpreter",
]
