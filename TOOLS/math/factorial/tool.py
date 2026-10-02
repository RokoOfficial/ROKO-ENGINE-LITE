#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `math.factorial`."""
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

def math_factorial(n: int) -> int:
    """
    Calcula o fatorial de um número.

    Raises:
        ValueError: Se o número for negativo
    """
    n = int(n)
    if n < 0:
        raise ValueError("Fatorial de número negativo não permitido")
    return math.factorial(n)

