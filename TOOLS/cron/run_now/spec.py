#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.run_now`."""
from __future__ import annotations
from .tool import cron_run_now
NAME = "cron.run_now"
CATEGORY = "cron"
DESCRIPTION = "Executa job agora"
PARAMETERS = ['user_id', 'job_id']
FN = cron_run_now
