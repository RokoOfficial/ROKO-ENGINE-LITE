#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `auth.register`."""
from __future__ import annotations
from .tool import auth_register
NAME = "auth.register"
CATEGORY = "auth"
DESCRIPTION = "Regista um novo utilizador"
PARAMETERS = ['username', 'email', 'password']
FN = auth_register
