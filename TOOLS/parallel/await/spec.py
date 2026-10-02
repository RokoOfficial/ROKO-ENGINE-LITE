#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.await`."""
from __future__ import annotations
from .tool import parallel_await
NAME = "parallel.await"
CATEGORY = "parallel"
DESCRIPTION = "Aguarda resultado de tarefa"
PARAMETERS = ['task_id', 'timeout']
FN = parallel_await
