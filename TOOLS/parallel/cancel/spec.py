#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.cancel`."""
from __future__ import annotations
from .tool import parallel_cancel
NAME = "parallel.cancel"
CATEGORY = "parallel"
DESCRIPTION = "Cancela tarefa pendente"
PARAMETERS = ['task_id']
FN = parallel_cancel
