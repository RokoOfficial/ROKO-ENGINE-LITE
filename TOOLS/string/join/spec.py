#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.join`."""
from __future__ import annotations

from .tool import string_join

NAME = "string.join"
CATEGORY = "string"
DESCRIPTION = "Junta lista em string"
PARAMETERS = ['items', 'separator']
FN = string_join
