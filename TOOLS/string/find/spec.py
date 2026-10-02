#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.find`."""
from __future__ import annotations

from .tool import string_find

NAME = "string.find"
CATEGORY = "string"
DESCRIPTION = "Encontra posição da substring"
PARAMETERS = ['text', 'substring']
FN = string_find
