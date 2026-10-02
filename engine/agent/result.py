#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Montagem do result de agent.run."""
from __future__ import annotations

from typing import Any, Dict, Optional


def make_result(
    *,
    ok: bool,
    run_id: str,
    response: Any = None,
    steps: int = 0,
    tools_used: int = 0,
    facts_extracted: int = 0,
    elapsed_ms: int = 0,
    stopped_reason: str = "return",
    error: Optional[str] = None,
    plan_label: str = "",
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "ok": ok,
        "run_id": run_id,
        "response": response,
        "steps": steps,
        "tools_used": tools_used,
        "facts_extracted": facts_extracted,
        "elapsed_ms": elapsed_ms,
        "stopped_reason": stopped_reason,
        "plan": plan_label,
    }
    if error:
        out["error"] = error
    return out
