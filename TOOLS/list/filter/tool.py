#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `list.filter`."""
from __future__ import annotations

from typing import Any, List, Optional, Union
import ast
import datetime as dt
import hashlib
import json
import math
import os
import random
import re
import time
import unicodedata
import uuid
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # type: ignore

REQUEST_TIMEOUT = 30
LOGS_FOLDER = Path(__file__).resolve().parents[3] / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

def list_filter(items: List[Any], condition: str) -> List[Any]:
    """
    Filtra a lista por uma condição simples.

    Exemplo: list_filter([1,2,3,4,5], ">3") -> [4,5]
    """
    items = list(items)
    result = []
    condition = condition.strip()

    if condition.startswith(">"):
        threshold = float(condition[1:].strip())
        return [x for x in items if isinstance(x, (int, float)) and float(x) > threshold]
    elif condition.startswith("<"):
        threshold = float(condition[1:].strip())
        return [x for x in items if isinstance(x, (int, float)) and float(x) < threshold]
    elif condition.startswith(">="):
        threshold = float(condition[2:].strip())
        return [x for x in items if isinstance(x, (int, float)) and float(x) >= threshold]
    elif condition.startswith("<="):
        threshold = float(condition[2:].strip())
        return [x for x in items if isinstance(x, (int, float)) and float(x) <= threshold]
    elif condition.startswith("=="):
        value = condition[2:].strip()
        return [x for x in items if str(x) == value]
    else:
        # Retorna itens que contenham a string
        return [x for x in items if condition.lower() in str(x).lower()]

