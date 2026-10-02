#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.execute`."""
from __future__ import annotations
from .tool import parallel_execute
NAME = "parallel.execute"
CATEGORY = "parallel"
DESCRIPTION = "Execucao sincrona paralela"
PARAMETERS = ['dados', 'operacao']
FN = parallel_execute
