#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.get_fact`."""
from __future__ import annotations
from .tool import memory_get_fact
NAME = "memory.get_fact"
CATEGORY = "memory"
DESCRIPTION = "Obtem um facto"
PARAMETERS = ['user_id', 'key']
FN = memory_get_fact
