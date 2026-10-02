#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent loop simbólico ROKO→ROKO (sem LLM).

Carrega um plan (.roko/.hmp), injecta goal/ctx/HGR, executa no interpretador,
grava steps no HGR e devolve result estruturado.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from engine.hgr import get_memory_agent
from engine.hgr.facade import MemoryEnhancedAgent
from engine.interpreter import RokoInterpreter

from .config import AgentConfig
from .context import build_run_variables
from .loader import load_plan
from .result import make_result


def _safe_record_batch(mem, uid, goal, batch, parallel_group):
    try:
        mem.record_steps_batch(uid, goal, batch, parallel_group=parallel_group)
    except Exception:
        pass


def _safe_record_step(mem, uid, goal, step):
    try:
        mem.record_step(uid, goal, step)
    except Exception:
        pass


def run_agent(
    plan: str,
    goal: str,
    *,
    id: Optional[str] = None,
    max_steps: Optional[int] = None,
    user_id: Optional[str] = None,
    vars: Optional[Dict[str, Any]] = None,
    config: Optional[AgentConfig] = None,
    memory: Optional[MemoryEnhancedAgent] = None,
) -> Dict[str, Any]:
    cfg = config or AgentConfig()
    run_id = (id or "").strip() or f"run-{uuid.uuid4().hex[:12]}"
    uid = (user_id or cfg.default_user_id).strip() or cfg.default_user_id
    limit = int(max_steps if max_steps is not None else cfg.default_max_steps)
    if limit < 1:
        limit = 1

    t0 = time.monotonic()
    mem = memory or get_memory_agent()

    try:
        source, plan_label = load_plan(plan)
    except Exception as e:
        return make_result(
            ok=False,
            run_id=run_id,
            response=None,
            steps=0,
            tools_used=0,
            elapsed_ms=int((time.monotonic() - t0) * 1000),
            stopped_reason="error",
            error=str(e),
            plan_label=str(plan),
        )

    try:
        mem.add_chat_message(uid, "user", goal)
    except Exception:
        pass

    tools_used = 0
    call_events: List[Dict[str, Any]] = []
    last_out: Dict[str, Any] = {}
    stopped_reason = "max_steps"
    final_response: Any = None
    step = 0
    script_error: Optional[str] = None

    def on_event(ev: Dict[str, Any]) -> None:
        nonlocal tools_used
        if ev.get("event") == "call" or ev.get("type") == "call":
            tools_used += 1
            call_events.append(dict(ev))

    try:
        while step < limit:
            step += 1
            call_events.clear()
            inject = build_run_variables(
                goal=goal,
                user_id=uid,
                run_id=run_id,
                step=step,
                max_steps=limit,
                memory=mem,
                extra=vars,
            )
            interp = RokoInterpreter()
            out = interp.execute(source, variables=inject, on_event=on_event)
            last_out = out

            batch = []
            for ev in call_events:
                tool = ev.get("tool") or ""
                result_val = ev.get("result")
                batch.append(
                    {
                        "thought": f"step={step} CALL {tool}",
                        "action": "tool_call",
                        "tool": tool,
                        "tool_used": tool,
                        "result": result_val,
                        "tool_result": result_val,
                        "params": ev.get("params"),
                        "tool_args": ev.get("params"),
                        "status": "success",
                        "confidence": 0.85,
                    }
                )
            if batch:
                _safe_record_batch(mem, uid, goal, batch, f"step-{step}")
            elif out.get("success"):
                _safe_record_step(
                    mem,
                    uid,
                    goal,
                    {
                        "thought": f"step={step} plan exec",
                        "action": "plan_step",
                        "status": "success",
                        "confidence": 0.6,
                        "result": str(out.get("return_value", ""))[:300],
                    },
                )

            if not out.get("success"):
                stopped_reason = "error"
                script_error = str(out.get("error") or out.get("message") or "script failed")
                final_response = {"error": script_error, "output": out.get("output")}
                _safe_record_step(
                    mem,
                    uid,
                    goal,
                    {
                        "thought": script_error[:300],
                        "action": "plan_error",
                        "status": "error",
                        "confidence": 0.5,
                        "result": script_error[:300],
                    },
                )
                break

            ret = out.get("return_value")
            if ret is not None:
                final_response = ret
                stopped_reason = "return"
                break
            for ev in out.get("trace") or []:
                if ev.get("type") == "return":
                    final_response = ev.get("value", ret)
                    stopped_reason = "return"
                    break
            if stopped_reason == "return":
                break

            if step >= limit:
                final_response = out.get("return_value")
                if final_response is None and out.get("output"):
                    final_response = out["output"][-1]
                stopped_reason = "max_steps" if final_response is None else "return"
                break

    except Exception as e:
        elapsed = int((time.monotonic() - t0) * 1000)
        return make_result(
            ok=False,
            run_id=run_id,
            response=None,
            steps=step,
            tools_used=tools_used,
            elapsed_ms=elapsed,
            stopped_reason="error",
            error=str(e),
            plan_label=plan_label,
        )

    facts_n = 0
    try:
        reply_txt = str(final_response) if final_response is not None else ""
        facts_n = int(mem.extract_and_store_facts(uid, goal, reply_txt) or 0)
    except Exception:
        facts_n = 0

    try:
        mem.add_chat_message(
            uid, "assistant", str(final_response)[:2000] if final_response is not None else ""
        )
    except Exception:
        pass
    _safe_record_step(
        mem,
        uid,
        goal,
        {
            "thought": str(final_response)[:300] if final_response is not None else "",
            "action": "final_answer",
            "status": "final",
            "confidence": 0.9,
            "result": str(final_response)[:300] if final_response is not None else "",
            "steps": step,
            "tools_used": tools_used,
        },
    )

    elapsed = int((time.monotonic() - t0) * 1000)
    ok = stopped_reason in ("return", "max_steps") and bool(last_out.get("success", True))
    if stopped_reason == "error":
        ok = False

    return make_result(
        ok=ok,
        run_id=run_id,
        response=final_response,
        steps=step,
        tools_used=tools_used,
        facts_extracted=facts_n,
        elapsed_ms=elapsed,
        stopped_reason=stopped_reason,
        error=script_error if not ok else None,
        plan_label=plan_label,
    )
