#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `log.print`."""
from __future__ import annotations

from typing import Any, List, Optional, Union
import ast
import datetime as dt
import hashlib
import json
import math
import os
import sys
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

def log_print(message: str, level: str = "INFO") -> str:
    """
    Registra uma mensagem no log.

    Args:
        message: Mensagem a ser registrada
        level: Nível do log (INFO, DEBUG, WARNING, ERROR)

    Returns:
        str: Mensagem registrada
    """
    timestamp = dt.datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry, file=sys.stdout)

    # Salva em arquivo de log
    try:
        log_file = LOGS_FOLDER / f"roko_{dt.datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except OSError:
        pass  # Ignora erro de escrita em arquivo

    return f"Logged: {message}"

