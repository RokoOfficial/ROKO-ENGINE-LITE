#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.status`."""
from __future__ import annotations

from .tool import http_status

NAME = "http.status"
CATEGORY = "http"
DESCRIPTION = "Verifica status HTTP"
PARAMETERS = ['url']
FN = http_status
