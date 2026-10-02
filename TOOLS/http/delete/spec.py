#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.delete`."""
from __future__ import annotations

from .tool import http_delete

NAME = "http.delete"
CATEGORY = "http"
DESCRIPTION = "Requisição HTTP DELETE"
PARAMETERS = ['url', 'headers']
FN = http_delete
