#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.slice`."""
from __future__ import annotations

from .tool import list_slice

NAME = "list.slice"
CATEGORY = "list"
DESCRIPTION = "Fatiamento de lista"
PARAMETERS = ['items', 'start', 'end']
FN = list_slice
