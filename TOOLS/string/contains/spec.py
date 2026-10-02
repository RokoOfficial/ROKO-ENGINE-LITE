#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.contains`."""
from __future__ import annotations

from .tool import string_contains

NAME = "string.contains"
CATEGORY = "string"
DESCRIPTION = "Verifica se contém substring"
PARAMETERS = ['text', 'substring']
FN = string_contains
