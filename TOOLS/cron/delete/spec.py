#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.delete`."""
from __future__ import annotations
from .tool import cron_delete
NAME = "cron.delete"
CATEGORY = "cron"
DESCRIPTION = "Remove job"
PARAMETERS = ['user_id', 'job_id']
FN = cron_delete
