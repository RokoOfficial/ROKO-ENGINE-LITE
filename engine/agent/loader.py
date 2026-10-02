#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrega planos ROKO (path Oracle/plans ou script inline)."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

_ROOT = Path(__file__).resolve().parents[2]


def load_plan(plan: str) -> Tuple[str, str]:
    """
    Resolve `plan` para (source, label).

    - Se for path existente (relativo à raiz do projeto ou absoluto), lê o ficheiro.
    - Se contiver quebras de linha ou keywords ROKO, trata como script inline.
    - Caso contrário tenta Oracle/ e plans/.
    """
    plan = (plan or "").strip()
    if not plan:
        raise ValueError("plan vazio")

    # inline script
    if "\n" in plan or plan.upper().lstrip().startswith(
        ("SET ", "CALL ", "IF ", "WHILE ", "FOR ", "RETURN", "//")
    ):
        return plan, "inline"

    candidates = [
        Path(plan),
        _ROOT / plan,
        _ROOT / "plans" / plan,
        _ROOT / "Oracle" / plan,
    ]
    # se só o nome do ficheiro
    if "/" not in plan and "\\" not in plan:
        candidates.extend(
            [
                _ROOT / "plans" / f"{plan}.roko",
                _ROOT / "plans" / f"{plan}.hmp",
                _ROOT / "Oracle" / f"{plan}.roko",
                _ROOT / "Oracle" / f"{plan}.hmp",
            ]
        )

    for p in candidates:
        try:
            if p.is_file():
                return p.read_text(encoding="utf-8"), str(p.relative_to(_ROOT) if _ROOT in p.parents or p.parent == _ROOT else p)
        except Exception:
            continue

    raise FileNotFoundError(f"Plan não encontrado: {plan}")
