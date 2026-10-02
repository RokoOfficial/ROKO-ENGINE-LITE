#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `cron.run_now`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def cron_run_now(user_id: str, job_id: int) -> Dict[str, Any]:
    from engine.hgr import get_memory_manager
    return get_memory_manager().crons.run_now(int(job_id), user_id)

