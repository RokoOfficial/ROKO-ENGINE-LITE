#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `date.parse`."""
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

def date_parse(date_str: str) -> str:
    """
    Tenta parsear uma data em diferentes formatos e retorna no formato ISO.
    """
    for fmt in [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y%m%d"
    ]:
        try:
            dt_obj = dt.datetime.strptime(str(date_str), fmt)
            return dt_obj.isoformat()
        except ValueError:
            continue
    raise ValueError(f"Não foi possível parsear a data: {date_str}")

