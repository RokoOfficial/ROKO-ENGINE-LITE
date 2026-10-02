#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `system.version`."""
from __future__ import annotations

from typing import Any


def system_version() -> str:
    """Retorna a versão do sistema / engine."""
    try:
        from TOOLS.registry import APP_VERSION, TOOL_VERSION
        return f"{APP_VERSION} (tools {TOOL_VERSION})"
    except Exception:
        return "2.3.1"
