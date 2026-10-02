#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuração do subsistema HGR (memória + auth + cron)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

_ROOT = Path(__file__).resolve().parents[2]
_DATA = _ROOT / "data"
_DATA.mkdir(parents=True, exist_ok=True)


@dataclass
class MemoryConfig:
    db_path: str = str(_DATA / "agent_memory.db")
    short_term_size: int = 30
    short_term_ttl: int = 3600
    medium_term_size: int = 100
    medium_term_ttl: int = 86400
    min_relevance_score: float = 0.05
    importance_threshold: float = 0.3
    max_chat_history: int = 200
    chat_history_to_llm: int = 40
    max_facts_in_prompt: int = 20
    cron_tick_interval: int = 30
    # v5 — agent loop simbólico / steps de erro
    persist_error_steps: bool = True
    error_importance_floor: float = 0.45
    max_parallel_steps_in_prompt: int = 8


@dataclass
class AuthConfig:
    db_path: str = str(_DATA / "users.db")
    jwt_secret: str = field(
        default_factory=lambda: os.environ.get("ROKO_JWT_SECRET", "roko-dev-secret-change-me")
    )
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    min_password_length: int = 8
    max_login_attempts: int = 5
    lockout_duration_seconds: int = 900
