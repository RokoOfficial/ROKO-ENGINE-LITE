#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `date.format`."""
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

def date_format(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formata uma data conforme o formato especificado."""
    try:
        dt_obj = dt.datetime.fromisoformat(str(date_str))
        return dt_obj.strftime(str(format_str))
    except ValueError:
        # Tenta parsear formatos comuns
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"]:
            try:
                dt_obj = dt.datetime.strptime(str(date_str), fmt)
                return dt_obj.strftime(str(format_str))
            except ValueError:
                continue
        raise ValueError(f"Formato de data inválido: {date_str}")

