#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `string.slice`."""
from __future__ import annotations

from .tool import string_slice

NAME = "string.slice"
CATEGORY = "string"
DESCRIPTION = "Fatiamento de string"
PARAMETERS = ['text', 'start', 'end']
FN = string_slice
