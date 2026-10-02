#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .enums import EstrategiaTipo, StatusExecucao, TipoBloco, TipoFila


@dataclass
class Bloco:
    id: int
    tipo: TipoBloco
    dados: List[Any]
    operacao: str = ""  # nome de tool ROKO, ex: "math.square" — aplicado a cada item
    independente: bool = True
    tamanho: int = 0
    nome: str = ""
    timeout: float = 30.0
    prioridade: int = 5
    metadados: Dict = field(default_factory=dict)

    def __post_init__(self):
        if self.tamanho == 0 and self.dados is not None:
            self.tamanho = len(self.dados)
        if not self.nome:
            self.nome = f"Bloco_{self.id}"


@dataclass
class ConfiguracaoFila:
    tipo: TipoFila = TipoFila.FIFO
    max_workers: int = 4
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 0.5


@dataclass
class Tarefa:
    id: int
    bloco: Bloco
    prioridade: int = 5
    deadline: Optional[float] = None
    tentativas: int = 0
    max_tentativas: int = 3
    status: StatusExecucao = StatusExecucao.PENDENTE
    resultado: Any = None
    erro: Optional[str] = None
    timestamp_criacao: float = field(default_factory=time.time)
    timestamp_inicio: float = 0.0
    timestamp_fim: float = 0.0
    fila_id: int = 0
    callback: Optional[Callable] = None


@dataclass
class Estrategia:
    tipo: EstrategiaTipo
    threads: int = 1
    chunk_size: int = 0
    motivo: str = ""
