#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.index`."""
from __future__ import annotations

from .tool import list_index

NAME = "list.index"
CATEGORY = "list"
DESCRIPTION = "Índice do item"
PARAMETERS = ['items', 'value']
FN = list_index
