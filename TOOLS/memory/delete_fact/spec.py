#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.delete_fact`."""
from __future__ import annotations
from .tool import memory_delete_fact
NAME = "memory.delete_fact"
CATEGORY = "memory"
DESCRIPTION = "Remove factos"
PARAMETERS = ['user_id', 'key', 'category', 'delete_all']
FN = memory_delete_fact
