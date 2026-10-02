#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `crypto.hash`."""
from __future__ import annotations

from .tool import crypto_hash

NAME = "crypto.hash"
CATEGORY = "crypto"
DESCRIPTION = "Gera hash SHA-256"
PARAMETERS = ['text']
FN = crypto_hash
