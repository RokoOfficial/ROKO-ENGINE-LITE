#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.get`."""
from __future__ import annotations

from .tool import http_get

NAME = "http.get"
CATEGORY = "http"
DESCRIPTION = "Requisição HTTP GET"
PARAMETERS = ['url', 'headers']
FN = http_get
