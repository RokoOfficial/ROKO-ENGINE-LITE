#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `agent.run` — loop simbólico ROKO→ROKO."""
from __future__ import annotations

from typing import Any, Dict, Optional, Union


def agent_run(
    plan: str,
    goal: str,
    id: str = "",
    max_steps: int = 8,
    user_id: str = "default",
    vars: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Corre um plan ROKO no agent loop simbólico (sem LLM).

    Args:
        plan: path (plans/... Oracle/...) ou script ROKO inline
        goal: objectivo textual
        id: run_id opcional
        max_steps: teto de iterações
        user_id: memória HGR
        vars: dict extra injectado no plan

    Returns:
        dict com ok, run_id, response, steps, tools_used, ...
    """
    from engine.agent import run_agent

    return run_agent(
        plan=plan,
        goal=goal,
        id=id or None,
        max_steps=int(max_steps or 8),
        user_id=user_id or "default",
        vars=vars if isinstance(vars, dict) else None,
    )
