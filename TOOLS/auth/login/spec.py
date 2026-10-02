#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `auth.login`."""
from __future__ import annotations
from .tool import auth_login
NAME = "auth.login"
CATEGORY = "auth"
DESCRIPTION = "Autentica utilizador e devolve token JWT"
PARAMETERS = ['username', 'password']
FN = auth_login
