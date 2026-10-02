#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `string.split`."""
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

def string_split(text: str, separator: str = " ") -> List[str]:
    """Divide a string em uma lista usando o separador."""
    return str(text).split(str(separator))

