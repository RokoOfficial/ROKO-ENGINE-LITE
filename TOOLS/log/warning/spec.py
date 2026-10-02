#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `log.warning`."""
from __future__ import annotations

from .tool import log_warning

NAME = "log.warning"
CATEGORY = "log"
DESCRIPTION = "Registra log WARNING"
PARAMETERS = ['message']
FN = log_warning
