#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.list`."""
from __future__ import annotations
from .tool import cron_list
NAME = "cron.list"
CATEGORY = "cron"
DESCRIPTION = "Lista jobs"
PARAMETERS = ['user_id', 'status']
FN = cron_list
