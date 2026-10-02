#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `auth.logout`."""
from __future__ import annotations
from .tool import auth_logout
NAME = "auth.logout"
CATEGORY = "auth"
DESCRIPTION = "Revoga um token JWT"
PARAMETERS = ['token']
FN = auth_logout
