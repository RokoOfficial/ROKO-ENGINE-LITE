#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.cancel`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_cancel(task_id: int) -> Dict[str, Any]:
    from engine.parallel import get_motor
    return {"ok": get_motor().cancel(int(task_id))}

