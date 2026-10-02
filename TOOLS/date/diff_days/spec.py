#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `date.diff_days`."""
from __future__ import annotations

from .tool import date_diff_days

NAME = "date.diff_days"
CATEGORY = "date"
DESCRIPTION = "Diferença em dias entre duas datas"
PARAMETERS = ['date1', 'date2']
FN = date_diff_days
