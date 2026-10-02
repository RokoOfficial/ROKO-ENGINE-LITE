#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `math.percentage`."""
from __future__ import annotations

from .tool import math_percentage

NAME = "math.percentage"
CATEGORY = "math"
DESCRIPTION = "Calcula a porcentagem"
PARAMETERS = ['value', 'total']
FN = math_percentage
