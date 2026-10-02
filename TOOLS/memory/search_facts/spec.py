#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.search_facts`."""
from __future__ import annotations
from .tool import memory_search_facts
NAME = "memory.search_facts"
CATEGORY = "memory"
DESCRIPTION = "Pesquisa factos"
PARAMETERS = ['user_id', 'term']
FN = memory_search_facts
