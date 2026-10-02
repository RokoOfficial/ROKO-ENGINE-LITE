#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.set`."""
from __future__ import annotations

from .tool import list_set

NAME = "list.set"
CATEGORY = "list"
DESCRIPTION = "Define item por índice"
PARAMETERS = ['items', 'index', 'value']
FN = list_set
