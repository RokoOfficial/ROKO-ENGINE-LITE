#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.record_step`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_record_step(user_id: str, query: str = "", thought: str = "", action: str = "", confidence: float = 0.5, tool: str = None, result: str = None) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    step = {"query": query or "", "thought": thought or "", "action": action or "", "confidence": float(confidence or 0.5), "tool": tool, "result": result}
    row_id = get_memory_manager().steps.store(user_id, step)
    return {"ok": True, "id": row_id, "stored": row_id is not None}

