#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `http.post`."""
from __future__ import annotations

from .tool import http_post

NAME = "http.post"
CATEGORY = "http"
DESCRIPTION = "Requisição HTTP POST"
PARAMETERS = ['url', 'data', 'headers']
FN = http_post
