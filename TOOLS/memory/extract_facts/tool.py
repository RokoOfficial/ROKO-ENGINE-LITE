#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.extract_facts`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_extract_facts(user_id: str, text: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    keys = get_memory_manager().facts.extract_from_text(user_id, text)
    return {"ok": True, "extracted": keys}

