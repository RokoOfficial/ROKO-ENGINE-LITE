#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.sort`."""
from __future__ import annotations

from .tool import list_sort

NAME = "list.sort"
CATEGORY = "list"
DESCRIPTION = "Ordena a lista"
PARAMETERS = ['items', 'reverse']
FN = list_sort
