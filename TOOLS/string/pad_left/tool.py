#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `string.pad_left`."""
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

def string_pad_left(text: str, length: int, char: str = " ") -> str:
    """Preenche a string à esquerda até o comprimento especificado."""
    return str(text).rjust(int(length), str(char)[0] if char else " ")

