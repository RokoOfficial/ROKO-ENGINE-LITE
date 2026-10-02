#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.get_all_facts`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_get_all_facts(user_id: str, min_importance: float = 0.0) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    facts = get_memory_manager().facts.get_all(user_id, float(min_importance or 0.0))
    return {"ok": True, "facts": facts, "count": len(facts)}

