#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `parallel.status`."""
from __future__ import annotations
from .tool import parallel_status
NAME = "parallel.status"
CATEGORY = "parallel"
DESCRIPTION = "Estado das filas"
PARAMETERS = ['queue_id']
FN = parallel_status
