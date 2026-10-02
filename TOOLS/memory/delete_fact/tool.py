#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.delete_fact`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_delete_fact(user_id: str, key: str = None, category: str = None, delete_all: bool = False) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    n = get_memory_manager().facts.delete(user_id, key=key, category=category, delete_all=bool(delete_all))
    return {"ok": True, "deleted": n}

