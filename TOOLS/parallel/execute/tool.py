#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.execute`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_execute(dados: list, operacao: str) -> Dict[str, Any]:
    from engine.parallel import get_motor
    try:
        result = get_motor().execute(list(dados or []), operacao)
        return {"ok": True, "result": result, "count": len(result) if isinstance(result, list) else 1}
    except Exception as e:
        return {"ok": False, "error": str(e)}

