#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `list.remove`."""
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

def list_remove(items: List[Any], item: Any) -> List[Any]:
    """Remove a primeira ocorrência do item da lista."""
    result = list(items)
    try:
        result.remove(item)
    except ValueError:
        pass  # Ignora se o item não existe
    return result

