#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.retrieve_context`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_retrieve_context(user_id: str, query: str, max_items: int = 5) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    steps = get_memory_manager().steps.retrieve_relevant(user_id, query, int(max_items or 5))
    return {"ok": True, "steps": steps, "count": len(steps)}

