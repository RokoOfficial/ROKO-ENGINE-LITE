#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `auth.logout`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def auth_logout(token: str) -> Dict[str, Any]:
    from engine.hgr import get_auth_manager
    return get_auth_manager().logout(token)

