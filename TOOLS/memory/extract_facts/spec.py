#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.extract_facts`."""
from __future__ import annotations
from .tool import memory_extract_facts
NAME = "memory.extract_facts"
CATEGORY = "memory"
DESCRIPTION = "Extrai factos de texto"
PARAMETERS = ['user_id', 'text']
FN = memory_extract_facts
