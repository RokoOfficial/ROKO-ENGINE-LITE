#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.ends_with`."""
from __future__ import annotations

from .tool import string_ends_with

NAME = "string.ends_with"
CATEGORY = "string"
DESCRIPTION = "Verifica sufixo"
PARAMETERS = ['text', 'suffix']
FN = string_ends_with
