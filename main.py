#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point do ROKO ENGINE LITE.

Garante que o diretório do projeto esteja no PYTHONPATH e sobe a API Quart.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from APP.api import app  # noqa: E402


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8989))
    debug_mode = os.environ.get("ROKO_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug_mode)
