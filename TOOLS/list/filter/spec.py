#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.filter`."""
from __future__ import annotations

from .tool import list_filter

NAME = "list.filter"
CATEGORY = "list"
DESCRIPTION = "Filtra a lista"
PARAMETERS = ['items', 'condition']
FN = list_filter
