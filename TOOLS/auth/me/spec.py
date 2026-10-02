#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `auth.me`."""
from __future__ import annotations
from .tool import auth_me
NAME = "auth.me"
CATEGORY = "auth"
DESCRIPTION = "Devolve dados do utilizador a partir do token"
PARAMETERS = ['token']
FN = auth_me
