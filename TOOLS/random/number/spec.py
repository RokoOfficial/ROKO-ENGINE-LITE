#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `random.number`."""
from __future__ import annotations

from .tool import random_number

NAME = "random.number"
CATEGORY = "random"
DESCRIPTION = "Número inteiro aleatório"
PARAMETERS = ['min_val', 'max_val']
FN = random_number
