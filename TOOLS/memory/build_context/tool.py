#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.build_context`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_build_context(user_id: str, query: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    ctx = get_memory_manager().build_system_context(user_id, query)
    return {"ok": True, "context": ctx}

