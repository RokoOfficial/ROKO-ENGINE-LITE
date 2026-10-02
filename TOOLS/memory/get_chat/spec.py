#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.get_chat`."""
from __future__ import annotations
from .tool import memory_get_chat
NAME = "memory.get_chat"
CATEGORY = "memory"
DESCRIPTION = "Obtem historico de chat"
PARAMETERS = ['user_id', 'last_n']
FN = memory_get_chat
