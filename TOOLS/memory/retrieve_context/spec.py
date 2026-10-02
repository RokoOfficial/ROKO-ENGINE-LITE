#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.retrieve_context`."""
from __future__ import annotations
from .tool import memory_retrieve_context
NAME = "memory.retrieve_context"
CATEGORY = "memory"
DESCRIPTION = "Recupera steps relevantes"
PARAMETERS = ['user_id', 'query', 'max_items']
FN = memory_retrieve_context
