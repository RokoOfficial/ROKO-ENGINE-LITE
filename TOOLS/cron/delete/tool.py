#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `cron.delete`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def cron_delete(user_id: str, job_id: int) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    return {"ok": get_memory_manager().crons.delete(int(job_id), user_id)}

