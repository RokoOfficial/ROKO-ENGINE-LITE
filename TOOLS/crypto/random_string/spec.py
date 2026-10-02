#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `crypto.random_string`."""
from __future__ import annotations

from .tool import crypto_random_string

NAME = "crypto.random_string"
CATEGORY = "crypto"
DESCRIPTION = "Gera string aleatória"
PARAMETERS = ['length']
FN = crypto_random_string
