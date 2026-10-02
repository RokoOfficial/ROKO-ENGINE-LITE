#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.info`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_info() -> Dict[str, Any]:
    from engine.parallel import get_motor
    return {"ok": True, "info": get_motor().info()}

