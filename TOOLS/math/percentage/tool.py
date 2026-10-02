#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `math.percentage`."""
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

def math_percentage(value: Union[int, float], total: Union[int, float]) -> float:
    """Calcula a porcentagem de value em relação a total."""
    return (float(value) / float(total)) * 100 if float(total) != 0 else 0

