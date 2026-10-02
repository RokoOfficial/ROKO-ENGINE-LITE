#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.store_fact`."""
from __future__ import annotations
from .tool import memory_store_fact
NAME = "memory.store_fact"
CATEGORY = "memory"
DESCRIPTION = "Guarda um facto chave-valor"
PARAMETERS = ['user_id', 'key', 'value', 'importance', 'category']
FN = memory_store_fact
