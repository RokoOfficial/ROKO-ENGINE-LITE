#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.status`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_status(queue_id: int = None) -> Dict[str, Any]:
    from engine.parallel import get_motor
    st = get_motor().status(int(queue_id) if queue_id is not None else None)
    return {"ok": True, "status": st}

