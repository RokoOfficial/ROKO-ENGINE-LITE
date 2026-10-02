#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.unique`."""
from __future__ import annotations

from .tool import list_unique

NAME = "list.unique"
CATEGORY = "list"
DESCRIPTION = "Remove duplicatas"
PARAMETERS = ['items']
FN = list_unique
