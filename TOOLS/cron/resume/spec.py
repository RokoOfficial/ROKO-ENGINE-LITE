#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.resume`."""
from __future__ import annotations
from .tool import cron_resume
NAME = "cron.resume"
CATEGORY = "cron"
DESCRIPTION = "Retoma job"
PARAMETERS = ['user_id', 'job_id']
FN = cron_resume
