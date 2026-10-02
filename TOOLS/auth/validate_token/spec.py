#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `auth.validate_token`."""
from __future__ import annotations
from .tool import auth_validate_token
NAME = "auth.validate_token"
CATEGORY = "auth"
DESCRIPTION = "Valida um token JWT"
PARAMETERS = ['token']
FN = auth_validate_token
