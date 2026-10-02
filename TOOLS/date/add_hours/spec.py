#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `date.add_hours`."""
from __future__ import annotations

from .tool import date_add_hours

NAME = "date.add_hours"
CATEGORY = "date"
DESCRIPTION = "Adiciona horas a uma data"
PARAMETERS = ['date_str', 'hours']
FN = date_add_hours
