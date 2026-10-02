#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `http.put`."""
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

def http_put(url: str, data: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> str:
    """Realiza uma requisição HTTP PUT."""
    headers = headers or {"Content-Type": "application/json"}
    response = requests.put(str(url), json=data, timeout=REQUEST_TIMEOUT, headers=headers)
    response.raise_for_status()
    return response.text

