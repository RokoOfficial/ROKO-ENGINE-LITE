#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `date.parse`."""
from __future__ import annotations

from .tool import date_parse

NAME = "date.parse"
CATEGORY = "date"
DESCRIPTION = "Parseia data em múltiplos formatos"
PARAMETERS = ['date_str']
FN = date_parse
