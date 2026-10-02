#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `cron.create`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def cron_create(user_id: str, name: str, schedule: str, task: str, description: str = "", task_type: str = "agent") -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    job = get_memory_manager().crons.create(user_id, name, schedule, task, description or "", task_type or "agent")
    return {"ok": True, "job": job}

