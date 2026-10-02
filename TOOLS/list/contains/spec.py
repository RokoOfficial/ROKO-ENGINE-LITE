#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.contains`."""
from __future__ import annotations

from .tool import list_contains

NAME = "list.contains"
CATEGORY = "list"
DESCRIPTION = "Verifica se contém item"
PARAMETERS = ['items', 'value']
FN = list_contains
