#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `memory.get_chat`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def memory_get_chat(user_id: str, last_n: int = 40) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    msgs = get_memory_manager().chat.get(user_id, int(last_n or 40))
    return {"ok": True, "messages": msgs, "count": len(msgs)}

