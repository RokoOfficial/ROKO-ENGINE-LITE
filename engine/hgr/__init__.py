#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HGR — Hierarchical Grounded Reasoning (memória + auth + cron)."""
from __future__ import annotations

from typing import Optional

from .auth import AuthManager
from .config import AuthConfig, MemoryConfig
from .facade import MemoryEnhancedAgent
from .manager import HierarchicalMemoryManager

_memory: Optional[HierarchicalMemoryManager] = None
_auth: Optional[AuthManager] = None


def get_memory_manager(config: Optional[MemoryConfig] = None) -> HierarchicalMemoryManager:
    global _memory
    if _memory is None:
        _memory = HierarchicalMemoryManager(config)
    return _memory


def get_auth_manager(config: Optional[AuthConfig] = None) -> AuthManager:
    global _auth
    if _auth is None:
        _auth = AuthManager(config)
    return _auth


def get_memory_agent(config: Optional[MemoryConfig] = None) -> MemoryEnhancedAgent:
    """Facade v5 sobre o manager singleton."""
    return MemoryEnhancedAgent(manager=get_memory_manager(config))


__all__ = [
    "MemoryConfig",
    "AuthConfig",
    "HierarchicalMemoryManager",
    "AuthManager",
    "MemoryEnhancedAgent",
    "get_memory_manager",
    "get_auth_manager",
    "get_memory_agent",
]
