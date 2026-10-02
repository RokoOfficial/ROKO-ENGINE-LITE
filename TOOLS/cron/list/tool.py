#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `cron.list`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def cron_list(user_id: str, status: str = None) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    jobs = get_memory_manager().crons.list_jobs(user_id, status)
    return {"ok": True, "jobs": jobs, "count": len(jobs)}

