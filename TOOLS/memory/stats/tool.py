#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.stats`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_stats(user_id: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    return {"ok": True, "stats": get_memory_manager().stats(user_id)}

