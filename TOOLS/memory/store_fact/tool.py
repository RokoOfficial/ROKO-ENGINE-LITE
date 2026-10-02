#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.store_fact`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_store_fact(user_id: str, key: str, value: str, importance: float = 0.5, category: str = "general") -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    created = get_memory_manager().facts.store(user_id, key, value, float(importance or 0.5), category or "general")
    return {"ok": True, "created": created, "key": key}

