#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.build_context`."""
from __future__ import annotations
from .tool import memory_build_context
NAME = "memory.build_context"
CATEGORY = "memory"
DESCRIPTION = "Monta contexto para system prompt"
PARAMETERS = ['user_id', 'query']
FN = memory_build_context
