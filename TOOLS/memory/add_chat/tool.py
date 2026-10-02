#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.add_chat`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_add_chat(user_id: str, role: str, content: str) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    row_id = get_memory_manager().chat.add(user_id, role, content)
    return {"ok": True, "id": row_id}

