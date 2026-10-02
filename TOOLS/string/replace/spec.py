#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.replace`."""
from __future__ import annotations

from .tool import string_replace

NAME = "string.replace"
CATEGORY = "string"
DESCRIPTION = "Substitui texto"
PARAMETERS = ['text', 'old', 'new']
FN = string_replace
