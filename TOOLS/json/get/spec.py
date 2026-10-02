#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `json.get`."""
from __future__ import annotations

from .tool import json_get

NAME = "json.get"
CATEGORY = "json"
DESCRIPTION = "Obtém valor por chave"
PARAMETERS = ['obj', 'key', 'default']
FN = json_get
