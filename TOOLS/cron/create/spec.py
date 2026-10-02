#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `cron.create`."""
from __future__ import annotations
from .tool import cron_create
NAME = "cron.create"
CATEGORY = "cron"
DESCRIPTION = "Cria job agendado"
PARAMETERS = ['user_id', 'name', 'schedule', 'task', 'description', 'task_type']
FN = cron_create
