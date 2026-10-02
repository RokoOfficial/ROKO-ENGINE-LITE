#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.prepend`."""
from __future__ import annotations

from .tool import list_prepend

NAME = "list.prepend"
CATEGORY = "list"
DESCRIPTION = "Adiciona item no início"
PARAMETERS = ['items', 'item']
FN = list_prepend
