#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from enum import Enum


class TipoBloco(Enum):
    FOR = "for"
    WHILE = "while"
    IF = "if"
    BASH = "bash"
    PYTHON = "python"


class EstrategiaTipo(Enum):
    SEQUENCIAL = "sequencial"
    PARALELO_TOTAL = "paralelo_total"
    PARALELO_PARCIAL = "paralelo_parcial"


class StatusExecucao(Enum):
    PENDENTE = "pendente"
    EXECUTANDO = "executando"
    CONCLUIDO = "concluido"
    FALHA = "falha"
    CANCELADO = "cancelado"
    TIMEOUT = "timeout"


class TipoFila(Enum):
    FIFO = "fifo"
    PRIORIDADE = "prioridade"
    DEADLINE = "deadline"
