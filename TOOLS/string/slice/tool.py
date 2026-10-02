#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `string.slice`."""
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

def string_slice(text: str, start: int, end: Optional[int] = None) -> str:
    """Fatiamento de string (slice)."""
    start = int(start)
    return str(text)[start:] if end is None else str(text)[start:int(end)]

