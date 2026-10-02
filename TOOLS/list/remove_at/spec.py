#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.remove_at`."""
from __future__ import annotations

from .tool import list_remove_at

NAME = "list.remove_at"
CATEGORY = "list"
DESCRIPTION = "Remove item por índice"
PARAMETERS = ['items', 'index']
FN = list_remove_at
