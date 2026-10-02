#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `log.debug`."""
from __future__ import annotations

from .tool import log_debug

NAME = "log.debug"
CATEGORY = "log"
DESCRIPTION = "Registra log DEBUG"
PARAMETERS = ['message']
FN = log_debug
