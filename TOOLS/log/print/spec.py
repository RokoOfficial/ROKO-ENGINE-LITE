#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `log.print`."""
from __future__ import annotations

from .tool import log_print

NAME = "log.print"
CATEGORY = "log"
DESCRIPTION = "Registra log INFO"
PARAMETERS = ['message', 'level']
FN = log_print
