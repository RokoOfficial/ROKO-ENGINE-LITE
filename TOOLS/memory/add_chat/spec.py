#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `memory.add_chat`."""
from __future__ import annotations
from .tool import memory_add_chat
NAME = "memory.add_chat"
CATEGORY = "memory"
DESCRIPTION = "Adiciona mensagem ao chat"
PARAMETERS = ['user_id', 'role', 'content']
FN = memory_add_chat
