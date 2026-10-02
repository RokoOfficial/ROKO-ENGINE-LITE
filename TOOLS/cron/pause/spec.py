#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.pause`."""
from __future__ import annotations
from .tool import cron_pause
NAME = "cron.pause"
CATEGORY = "cron"
DESCRIPTION = "Pausa job"
PARAMETERS = ['user_id', 'job_id']
FN = cron_pause
