#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `string.find`."""
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

def string_find(text: str, substring: str) -> int:
    """
    Encontra a posição da primeira ocorrência do substring.

    Returns:
        int: Posição encontrada ou -1 se não encontrado
    """
    return str(text).find(str(substring))

