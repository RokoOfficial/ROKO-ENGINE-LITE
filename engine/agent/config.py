#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Defaults do agent loop simbólico ROKO→ROKO."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentConfig:
    default_max_steps: int = 8
    default_user_id: str = "default"
    tool_timeout_seconds: int = 45
    max_parallel_tools: int = 8
