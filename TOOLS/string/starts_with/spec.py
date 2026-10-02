#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.starts_with`."""
from __future__ import annotations

from .tool import string_starts_with

NAME = "string.starts_with"
CATEGORY = "string"
DESCRIPTION = "Verifica prefixo"
PARAMETERS = ['text', 'prefix']
FN = string_starts_with
