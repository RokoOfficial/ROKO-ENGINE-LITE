#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `list.remove_at`."""
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

def list_remove_at(items: List[Any], index: int) -> List[Any]:
    """Remove o item na posição especificada."""
    result = list(items)
    try:
        del result[int(index)]
    except IndexError:
        pass
    return result

