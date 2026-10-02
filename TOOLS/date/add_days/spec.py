#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `date.add_days`."""
from __future__ import annotations

from .tool import date_add_days

NAME = "date.add_days"
CATEGORY = "date"
DESCRIPTION = "Adiciona dias a uma data"
PARAMETERS = ['date_str', 'days']
FN = date_add_days
