#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.append`."""
from __future__ import annotations

from .tool import list_append

NAME = "list.append"
CATEGORY = "list"
DESCRIPTION = "Adiciona item ao final"
PARAMETERS = ['items', 'item']
FN = list_append
