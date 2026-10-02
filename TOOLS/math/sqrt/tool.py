#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `math.sqrt`."""
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

def math_sqrt(a: Union[int, float]) -> float:
    """
    Calcula a raiz quadrada.

    Raises:
        ValueError: Se o número for negativo
    """
    value = float(a)
    if value < 0:
        raise ValueError("Raiz quadrada de número negativo não permitida")
    return math.sqrt(value)

