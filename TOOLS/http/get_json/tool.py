#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `http.get_json`."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
import json
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # type: ignore

REQUEST_TIMEOUT = 30
LOGS_FOLDER = Path(__file__).resolve().parents[3] / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


def http_get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Realiza uma requisição HTTP GET e retorna o JSON parseado."""
    if requests is None:
        raise RuntimeError("requests library is required for http.get_json")
    headers = headers or {}
    response = requests.get(str(url), timeout=REQUEST_TIMEOUT, headers=headers)
    response.raise_for_status()
    return response.json()
