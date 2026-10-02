#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metadados da tool `agent.run`."""
from __future__ import annotations

from .tool import agent_run

NAME = "agent.run"
CATEGORY = "agent"
DESCRIPTION = "Loop agentico simbolico ROKO→ROKO (plan + goal + HGR, sem LLM)"
PARAMETERS = ["plan", "goal", "id", "max_steps", "user_id", "vars"]
FN = agent_run
