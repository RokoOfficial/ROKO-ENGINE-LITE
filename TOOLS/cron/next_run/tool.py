#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `cron.next_run`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def cron_next_run(user_id: str, job_id: int) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    job = get_memory_manager().crons.get(int(job_id), user_id)
    if not job:
        return {"ok": False, "error": "job not found"}
    return {"ok": True, "next_run": get_memory_manager().crons.format_next_run(job), "job": job}

