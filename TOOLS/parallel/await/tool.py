#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.await`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_await(task_id: int, timeout: float = 30.0) -> Dict[str, Any]:
    from engine.parallel import get_motor
    try:
        result = get_motor().aguardar(int(task_id), float(timeout or 30))
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}

