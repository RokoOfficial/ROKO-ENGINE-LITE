#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.clear_chat`."""
from __future__ import annotations
from .tool import memory_clear_chat
NAME = "memory.clear_chat"
CATEGORY = "memory"
DESCRIPTION = "Limpa historico de chat"
PARAMETERS = ['user_id']
FN = memory_clear_chat
