#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.record_step`."""
from __future__ import annotations
from .tool import memory_record_step
NAME = "memory.record_step"
CATEGORY = "memory"
DESCRIPTION = "Regista step de raciocinio"
PARAMETERS = ['user_id', 'query', 'thought', 'action', 'confidence', 'tool', 'result']
FN = memory_record_step
