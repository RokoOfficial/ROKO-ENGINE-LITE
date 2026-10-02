#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.report`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_report() -> Dict[str, Any]:
    from engine.parallel import get_motor
    return get_motor().report()

