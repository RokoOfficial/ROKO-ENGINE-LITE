#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta variáveis injectadas no interpretador para o plan."""
from __future__ import annotations

from typing import Any, Dict, Optional

from engine.hgr.facade import MemoryEnhancedAgent


def build_run_variables(
    *,
    goal: str,
    user_id: str,
    run_id: str,
    step: int,
    max_steps: int,
    memory: MemoryEnhancedAgent,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ctx = memory.build_context(user_id, goal)
    vars_: Dict[str, Any] = {
        "goal": goal,
        "user_id": user_id,
        "run_id": run_id,
        "step": step,
        "max_steps": max_steps,
        "ctx": ctx or "",
        "has_context": bool(ctx and ctx.strip()),
    }
    if extra:
        vars_.update(extra)
    return vars_
