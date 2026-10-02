#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.get`."""
from __future__ import annotations

from .tool import list_get

NAME = "list.get"
CATEGORY = "list"
DESCRIPTION = "Obtém item por índice"
PARAMETERS = ['items', 'index']
FN = list_get
