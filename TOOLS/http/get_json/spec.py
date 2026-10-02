#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.get_json`."""
from __future__ import annotations

from .tool import http_get_json

NAME = "http.get_json"
CATEGORY = "http"
DESCRIPTION = "HTTP GET com retorno JSON"
PARAMETERS = ['url', 'headers']
FN = http_get_json
