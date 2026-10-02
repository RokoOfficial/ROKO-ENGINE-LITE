#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.create_queue`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_create_queue(name: str = "default", tipo: str = "fifo", max_workers: int = 4, timeout: float = 30.0) -> Dict[str, Any]:
    from engine.parallel import get_motor
    qid = get_motor().criar_fila(name or "default", tipo or "fifo", int(max_workers or 4), float(timeout or 30))
    return {"ok": True, "queue_id": qid}

