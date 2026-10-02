#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `json.set`."""
from __future__ import annotations

from .tool import json_set

NAME = "json.set"
CATEGORY = "json"
DESCRIPTION = "Define valor por chave"
PARAMETERS = ['obj', 'key', 'value']
FN = json_set
