#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `log.error`."""
from __future__ import annotations

from .tool import log_error

NAME = "log.error"
CATEGORY = "log"
DESCRIPTION = "Registra log ERROR"
PARAMETERS = ['message']
FN = log_error
