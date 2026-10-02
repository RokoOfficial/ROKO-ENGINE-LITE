#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.next_run`."""
from __future__ import annotations
from .tool import cron_next_run
NAME = "cron.next_run"
CATEGORY = "cron"
DESCRIPTION = "Proxima execucao formatada"
PARAMETERS = ['user_id', 'job_id']
FN = cron_next_run
