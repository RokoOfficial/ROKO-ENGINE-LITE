#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.put`."""
from __future__ import annotations

from .tool import http_put

NAME = "http.put"
CATEGORY = "http"
DESCRIPTION = "Requisição HTTP PUT"
PARAMETERS = ['url', 'data', 'headers']
FN = http_put
