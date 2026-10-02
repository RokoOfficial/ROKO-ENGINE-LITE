#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.submit`."""
from __future__ import annotations
from .tool import parallel_submit
NAME = "parallel.submit"
CATEGORY = "parallel"
DESCRIPTION = "Submete trabalho paralelo"
PARAMETERS = ['dados', 'operacao', 'queue_id', 'prioridade', 'deadline']
FN = parallel_submit
