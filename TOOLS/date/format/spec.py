#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `date.format`."""
from __future__ import annotations

from .tool import date_format

NAME = "date.format"
CATEGORY = "date"
DESCRIPTION = "Formata data"
PARAMETERS = ['date_str', 'format_str']
FN = date_format
