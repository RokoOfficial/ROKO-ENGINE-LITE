#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.search_facts`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_search_facts(user_id: str, term: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    results = get_memory_manager().facts.search(user_id, term)
    return {"ok": True, "results": results, "count": len(results)}

