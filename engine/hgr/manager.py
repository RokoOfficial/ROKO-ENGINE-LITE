#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Orquestrador HierarchicalMemoryManager."""
from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict, Optional

from .chat import ChatHistoryManager
from .config import MemoryConfig
from .cron import CronManager
from .database import HGRDatabase
from .facts import FactsManager
from .steps import ContextStepsManager


class HierarchicalMemoryManager:
    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.db = HGRDatabase(self.config.db_path)
        self.facts = FactsManager(self.db, self.config.max_facts_in_prompt)
        self.chat = ChatHistoryManager(self.db, self.config.max_chat_history)
        self.steps = ContextStepsManager(
            self.db,
            self.config.importance_threshold,
            self.config.min_relevance_score,
            error_importance_floor=self.config.error_importance_floor,
            persist_error_steps=self.config.persist_error_steps,
            max_parallel_in_prompt=self.config.max_parallel_steps_in_prompt,
        )
        self.crons = CronManager(self.db)

    def session_id(self, user_id: str) -> str:
        day = datetime.utcnow().strftime("%Y-%m-%d")
        return hashlib.md5(f"{user_id}:{day}".encode()).hexdigest()[:16]

    def build_system_context(self, user_id: str, query: str) -> str:
        parts = []
        facts_block = self.facts.format_for_prompt(user_id)
        if facts_block:
            parts.append(facts_block)
        steps_block = self.steps.format_for_prompt(user_id, query)
        if steps_block:
            parts.append(steps_block)
        return "\n\n".join(parts)

    def stats(self, user_id: str) -> Dict[str, Any]:
        fact_stats = self.facts.stats(user_id)
        chat_count = self.db.fetchone(
            "SELECT COUNT(*) as c FROM chat_log WHERE user_id=?", (user_id,)
        )
        step_count = self.db.fetchone(
            "SELECT COUNT(*) as c FROM context_steps WHERE user_id=?", (user_id,)
        )
        cron_count = self.db.fetchone(
            "SELECT COUNT(*) as c FROM cron_jobs WHERE user_id=?", (user_id,)
        )
        return {
            "facts": fact_stats,
            "chat_messages": chat_count["c"] if chat_count else 0,
            "context_steps": step_count["c"] if step_count else 0,
            "cron_jobs": cron_count["c"] if cron_count else 0,
            "session_id": self.session_id(user_id),
        }
