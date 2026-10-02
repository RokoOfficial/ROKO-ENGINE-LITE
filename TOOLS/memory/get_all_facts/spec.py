#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.get_all_facts`."""
from __future__ import annotations
from .tool import memory_get_all_facts
NAME = "memory.get_all_facts"
CATEGORY = "memory"
DESCRIPTION = "Lista todos os factos"
PARAMETERS = ['user_id', 'min_importance']
FN = memory_get_all_facts
