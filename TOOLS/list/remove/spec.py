#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.remove`."""
from __future__ import annotations

from .tool import list_remove

NAME = "list.remove"
CATEGORY = "list"
DESCRIPTION = "Remove item da lista"
PARAMETERS = ['items', 'item']
FN = list_remove
