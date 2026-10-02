#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `random.choice`."""
from __future__ import annotations

from .tool import random_choice

NAME = "random.choice"
CATEGORY = "random"
DESCRIPTION = "Escolhe item aleatório"
PARAMETERS = ['items']
FN = random_choice
