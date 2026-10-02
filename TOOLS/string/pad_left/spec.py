#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.pad_left`."""
from __future__ import annotations

from .tool import string_pad_left

NAME = "string.pad_left"
CATEGORY = "string"
DESCRIPTION = "Preenche à esquerda"
PARAMETERS = ['text', 'length', 'char']
FN = string_pad_left
