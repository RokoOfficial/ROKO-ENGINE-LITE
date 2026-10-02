#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `math.max`."""
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

def math_max(*args: Union[int, float]) -> float:
    """
    Retorna o maior valor entre os argumentos.

    Raises:
        ValueError: Se nenhum argumento for fornecido
    """
    if not args:
        raise ValueError("math.max requer pelo menos um argumento")
    return max(float(x) for x in args)

