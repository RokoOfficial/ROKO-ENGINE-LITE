#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.count`."""
from __future__ import annotations

from .tool import string_count

NAME = "string.count"
CATEGORY = "string"
DESCRIPTION = "Conta ocorrências"
PARAMETERS = ['text', 'substring']
FN = string_count
