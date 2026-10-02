#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.get_fact`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_get_fact(user_id: str, key: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    fact = get_memory_manager().facts.get(user_id, key)
    return {"ok": fact is not None, "fact": fact}

