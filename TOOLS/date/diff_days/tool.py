#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `date.diff_days`."""
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

def date_diff_days(date1: str, date2: str) -> int:
    """Calcula a diferença em dias entre duas datas."""
    dt1 = dt.datetime.fromisoformat(str(date1))
    dt2 = dt.datetime.fromisoformat(str(date2))
    return abs((dt2 - dt1).days)

