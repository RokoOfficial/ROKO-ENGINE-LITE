#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Motor Parallel integrado ao ROKO ENGINE LITE."""
from __future__ import annotations

from typing import Optional

from .motor import MotorParallel

_motor: Optional[MotorParallel] = None


def get_motor() -> MotorParallel:
    global _motor
    if _motor is None:
        _motor = MotorParallel()
    return _motor


__all__ = ["MotorParallel", "get_motor"]
