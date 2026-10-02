#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facade MemoryEnhancedAgent — API estável para o agent loop simbólico.
Delega no HierarchicalMemoryManager modular do ROKO.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .config import MemoryConfig
from .manager import HierarchicalMemoryManager


class MemoryEnhancedAgent:
    """API estilo HGR v5 para o loop agentic ROKO→ROKO."""

    def __init__(self, config: Optional[MemoryConfig] = None, manager: Optional[HierarchicalMemoryManager] = None):
        if manager is not None:
            self.mgr = manager
            self.config = manager.config
        else:
            self.config = config or MemoryConfig()
            self.mgr = HierarchicalMemoryManager(self.config)

    def build_context(self, user_id: str, query: str) -> str:
        return self.mgr.build_system_context(user_id, query)

    def get_chat_history(self, user_id: str, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        n = last_n if last_n is not None else self.config.chat_history_to_llm
        return self.mgr.chat.get(user_id, last_n=n)

    def add_chat_message(self, user_id: str, role: str, content: str) -> int:
        return self.mgr.chat.add(user_id, role, content)

    def record_step(self, user_id: str, query: str, step: Dict[str, Any]) -> Optional[int]:
        data = dict(step)
        data.setdefault("query", query)
        return self.mgr.steps.store(user_id, data)

    def record_steps_batch(
        self,
        user_id: str,
        query: str,
        items: List[Dict[str, Any]],
        parallel_group: str = "",
    ) -> List[Optional[int]]:
        return self.mgr.steps.record_steps_batch(user_id, query, items, parallel_group=parallel_group)

    def extract_and_store_facts(
        self, user_id: str, user_msg: str, bot_reply: str = ""
    ) -> int:
        text = f"{user_msg}\n{bot_reply}"
        found = self.mgr.facts.extract_from_text(user_id, text)
        return len(found) if found else 0

    def store_fact(
        self, user_id: str, key: str, value: str, importance: float = 0.7, category: str = "general"
    ) -> Any:
        return self.mgr.facts.store(user_id, key, value, importance=importance, category=category)

    def stats(self, user_id: str) -> Dict[str, Any]:
        return self.mgr.stats(user_id)
