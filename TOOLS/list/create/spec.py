#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `list.create`."""
from __future__ import annotations

from .tool import list_create

NAME = "list.create"
CATEGORY = "list"
DESCRIPTION = "Cria uma lista"
PARAMETERS = ['items...']
FN = list_create
