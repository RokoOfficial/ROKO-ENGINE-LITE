#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.stats`."""
from __future__ import annotations
from .tool import memory_stats
NAME = "memory.stats"
CATEGORY = "memory"
DESCRIPTION = "Estatisticas de memoria"
PARAMETERS = ['user_id']
FN = memory_stats
