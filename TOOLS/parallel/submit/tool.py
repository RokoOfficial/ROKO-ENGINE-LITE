#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implementação da tool `parallel.submit`."""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

def parallel_submit(dados: list, operacao: str, queue_id: int = None, prioridade: int = 5, deadline: float = None) -> Dict[str, Any]:
    from engine.parallel import get_motor
    tid = get_motor().submit(list(dados or []), operacao, queue_id=int(queue_id) if queue_id is not None else None, prioridade=int(prioridade or 5), deadline=float(deadline) if deadline is not None else None)
    return {"ok": True, "task_id": tid}

