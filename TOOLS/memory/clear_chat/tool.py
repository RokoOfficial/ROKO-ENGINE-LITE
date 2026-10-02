#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.clear_chat`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_clear_chat(user_id: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    n = get_memory_manager().chat.clear(user_id)
    return {"ok": True, "deleted": n}

