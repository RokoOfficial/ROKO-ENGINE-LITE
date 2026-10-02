#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.create_queue`."""
from __future__ import annotations
from .tool import parallel_create_queue
NAME = "parallel.create_queue"
CATEGORY = "parallel"
DESCRIPTION = "Cria fila de execucao"
PARAMETERS = ['name', 'tipo', 'max_workers', 'timeout']
FN = parallel_create_queue
