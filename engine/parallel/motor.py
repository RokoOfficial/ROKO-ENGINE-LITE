#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Motor Parallel — filas + decisão + execução via tools ROKO."""
from __future__ import annotations

import heapq
import multiprocessing
import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .enums import EstrategiaTipo, StatusExecucao, TipoBloco, TipoFila
from .models import Bloco, ConfiguracaoFila, Estrategia, Tarefa


class MotorDecisao:
    def __init__(self):
        self.cores = multiprocessing.cpu_count()
        self._stats = {"python": 0, "paralelo": 0, "sequencial": 0}

    def decidir(self, bloco: Bloco) -> Estrategia:
        if bloco.independente and bloco.tamanho > 50:
            self._stats["paralelo"] += 1
            threads = min(self.cores, max(1, bloco.tamanho // 50 + 1), 8)
            return Estrategia(
                EstrategiaTipo.PARALELO_TOTAL,
                threads=threads,
                chunk_size=max(1, bloco.tamanho // threads),
                motivo=f"Paralelo total: {bloco.tamanho} itens",
            )
        if bloco.independente and bloco.tamanho > 10:
            self._stats["paralelo"] += 1
            threads = max(1, self.cores // 2)
            return Estrategia(
                EstrategiaTipo.PARALELO_PARCIAL,
                threads=threads,
                chunk_size=max(1, bloco.tamanho // threads),
                motivo=f"Paralelo parcial: {bloco.tamanho} itens",
            )
        self._stats["sequencial"] += 1
        return Estrategia(EstrategiaTipo.SEQUENCIAL, threads=1, motivo="Sequencial")


def _resolve_item_fn(operacao: str) -> Callable[[Any], Any]:
    """Resolve uma tool ROKO e devolve função item -> result."""
    # Import lazy para evitar ciclo no startup
    from TOOLS.registry import execute_tool, TOOL_SPECS

    op = (operacao or "").strip()
    if not op:
        return lambda x: x

    # Tools com um parâmetro "principal"
    # Convenção: passamos o item como primeiro parâmetro conhecido, ou como "value"/"x"/"text"/"n"
    def apply_item(item: Any) -> Any:
        spec = TOOL_SPECS.get(op)
        if spec is None:
            # tenta meta / fallback
            res = execute_tool(op, {"value": item, "x": item, "n": item, "text": item, "a": item})
            if res.get("success"):
                return res.get("result")
            raise RuntimeError(res.get("error", f"tool {op} failed"))

        params_list = spec.get("parameters") or []
        if not params_list:
            res = execute_tool(op, {})
        elif len(params_list) == 1:
            res = execute_tool(op, {params_list[0]: item})
        else:
            # multi-param: assume item é dict ou usa primeiro param
            if isinstance(item, dict):
                res = execute_tool(op, item)
            else:
                res = execute_tool(op, {params_list[0]: item})
        if not res.get("success"):
            raise RuntimeError(res.get("error", "tool error"))
        return res.get("result")

    return apply_item


class Executor:
    def __init__(self, motor: "MotorParallel"):
        self.motor = motor
        self._resultados_cache: Dict[int, Any] = {}

    def executar_estrategia(
        self, bloco: Bloco, estrategia: Estrategia, tarefa_id: Optional[int] = None
    ) -> List[Any]:
        if not bloco.dados:
            return []
        fn = _resolve_item_fn(bloco.operacao)
        try:
            if estrategia.tipo in (
                EstrategiaTipo.PARALELO_TOTAL,
                EstrategiaTipo.PARALELO_PARCIAL,
            ):
                with ThreadPoolExecutor(max_workers=estrategia.threads) as pool:
                    resultado = list(pool.map(fn, bloco.dados))
            else:
                resultado = [fn(item) for item in bloco.dados]
            if tarefa_id is not None:
                self._resultados_cache[tarefa_id] = resultado
            return resultado
        except Exception as e:
            raise RuntimeError(str(e)) from e


class FilaBase:
    def __init__(self, nome: str, config: ConfiguracaoFila, fila_id: int):
        self.nome = nome
        self.config = config
        self.fila_id = fila_id
        self._lock = threading.Lock()
        self._executor: Optional[Executor] = None
        self._workers: List[threading.Thread] = []
        self._rodando = False
        self._tarefas_concluidas: Dict[int, Any] = {}
        self._stats = {
            "total_adicionadas": 0,
            "total_concluidas": 0,
            "total_falhas": 0,
            "total_canceladas": 0,
            "total_timeouts": 0,
            "total_retries": 0,
        }

    def set_executor(self, executor: Executor) -> None:
        self._executor = executor

    def adicionar(self, tarefa: Tarefa) -> None:
        raise NotImplementedError

    def obter_proxima(self) -> Optional[Tarefa]:
        raise NotImplementedError

    def cancelar(self, tarefa_id: int) -> bool:
        raise NotImplementedError

    def obter_resultado(self, tarefa_id: int) -> Any:
        with self._lock:
            return self._tarefas_concluidas.get(tarefa_id)

    def iniciar(self) -> None:
        if self._rodando or not self._executor:
            return
        self._rodando = True
        for i in range(self.config.max_workers):
            t = threading.Thread(
                target=self._worker_loop,
                args=(f"w_{self.fila_id}_{i}",),
                daemon=True,
            )
            t.start()
            self._workers.append(t)

    def _worker_loop(self, worker_id: str) -> None:
        while self._rodando:
            try:
                tarefa = self.obter_proxima()
                if tarefa is None:
                    time.sleep(0.01)
                    continue
                if tarefa.deadline and time.time() > tarefa.deadline:
                    tarefa.status = StatusExecucao.TIMEOUT
                    self._stats["total_timeouts"] += 1
                    continue
                tarefa.status = StatusExecucao.EXECUTANDO
                tarefa.timestamp_inicio = time.time()
                try:
                    assert self._executor is not None
                    estrategia = self._executor.motor.motor_decisao.decidir(tarefa.bloco)
                    resultado = self._executor.executar_estrategia(
                        tarefa.bloco, estrategia, tarefa.id
                    )
                    tarefa.resultado = resultado if resultado is not None else []
                    tarefa.status = StatusExecucao.CONCLUIDO
                    self._stats["total_concluidas"] += 1
                    with self._lock:
                        self._tarefas_concluidas[tarefa.id] = tarefa.resultado
                    if tarefa.callback:
                        try:
                            tarefa.callback(tarefa)
                        except Exception:
                            pass
                except Exception as e:
                    tarefa.erro = str(e)
                    tarefa.tentativas += 1
                    self._stats["total_retries"] += 1
                    if tarefa.tentativas < tarefa.max_tentativas:
                        tarefa.status = StatusExecucao.PENDENTE
                        time.sleep(self.config.retry_delay)
                        self.adicionar(tarefa)
                    else:
                        tarefa.status = StatusExecucao.FALHA
                        self._stats["total_falhas"] += 1
                tarefa.timestamp_fim = time.time()
            except Exception:
                time.sleep(0.5)

    def get_status(self) -> Dict:
        with self._lock:
            return {
                "nome": self.nome,
                "fila_id": self.fila_id,
                "tipo": self.config.tipo.value,
                "tamanho_pendente": self._pending_size(),
                "workers_ativos": len([w for w in self._workers if w.is_alive()]),
                "max_workers": self.config.max_workers,
                "stats": self._stats.copy(),
            }

    def _pending_size(self) -> int:
        return 0


class FilaFIFO(FilaBase):
    def __init__(self, nome, config, fila_id):
        super().__init__(nome, config, fila_id)
        self._fila: deque = deque()

    def adicionar(self, tarefa: Tarefa) -> None:
        with self._lock:
            self._fila.append(tarefa)
            self._stats["total_adicionadas"] += 1

    def obter_proxima(self) -> Optional[Tarefa]:
        with self._lock:
            if self._fila:
                return self._fila.popleft()
        return None

    def cancelar(self, tarefa_id: int) -> bool:
        with self._lock:
            for i, t in enumerate(self._fila):
                if t.id == tarefa_id and t.status == StatusExecucao.PENDENTE:
                    t.status = StatusExecucao.CANCELADO
                    del self._fila[i]
                    self._stats["total_canceladas"] += 1
                    return True
        return False

    def _pending_size(self) -> int:
        return len(self._fila)


class FilaPrioridade(FilaBase):
    def __init__(self, nome, config, fila_id):
        super().__init__(nome, config, fila_id)
        self._heap: List = []
        self._contador = 0

    def adicionar(self, tarefa: Tarefa) -> None:
        with self._lock:
            heapq.heappush(self._heap, (tarefa.prioridade, self._contador, tarefa))
            self._contador += 1
            self._stats["total_adicionadas"] += 1

    def obter_proxima(self) -> Optional[Tarefa]:
        with self._lock:
            if self._heap:
                _, _, tarefa = heapq.heappop(self._heap)
                return tarefa
        return None

    def cancelar(self, tarefa_id: int) -> bool:
        with self._lock:
            new_heap = []
            found = False
            for item in self._heap:
                t = item[2]
                if t.id == tarefa_id and t.status == StatusExecucao.PENDENTE:
                    t.status = StatusExecucao.CANCELADO
                    found = True
                    self._stats["total_canceladas"] += 1
                else:
                    new_heap.append(item)
            if found:
                heapq.heapify(new_heap)
                self._heap = new_heap
            return found

    def _pending_size(self) -> int:
        return len(self._heap)


class FilaDeadline(FilaBase):
    def __init__(self, nome, config, fila_id):
        super().__init__(nome, config, fila_id)
        self._heap: List = []
        self._contador = 0

    def adicionar(self, tarefa: Tarefa) -> None:
        with self._lock:
            if tarefa.deadline is None:
                tarefa.deadline = time.time() + self.config.timeout
            heapq.heappush(self._heap, (tarefa.deadline, self._contador, tarefa))
            self._contador += 1
            self._stats["total_adicionadas"] += 1

    def obter_proxima(self) -> Optional[Tarefa]:
        with self._lock:
            if self._heap:
                deadline, _, tarefa = heapq.heappop(self._heap)
                if time.time() > deadline:
                    tarefa.status = StatusExecucao.TIMEOUT
                    self._stats["total_timeouts"] += 1
                    return None
                return tarefa
        return None

    def cancelar(self, tarefa_id: int) -> bool:
        with self._lock:
            new_heap = []
            found = False
            for item in self._heap:
                t = item[2]
                if t.id == tarefa_id and t.status == StatusExecucao.PENDENTE:
                    t.status = StatusExecucao.CANCELADO
                    found = True
                    self._stats["total_canceladas"] += 1
                else:
                    new_heap.append(item)
            if found:
                heapq.heapify(new_heap)
                self._heap = new_heap
            return found

    def _pending_size(self) -> int:
        return len(self._heap)


class GerenciadorFilas:
    def __init__(self):
        self._filas: Dict[int, FilaBase] = {}
        self._proximo_fila_id = 0
        self._proximo_tarefa_id = 0
        self._lock = threading.Lock()
        self._executor: Optional[Executor] = None

    def set_executor(self, executor: Executor) -> None:
        self._executor = executor
        for f in self._filas.values():
            f.set_executor(executor)

    def criar_fila(self, nome: str, config: ConfiguracaoFila) -> int:
        with self._lock:
            fila_id = self._proximo_fila_id
            self._proximo_fila_id += 1
            if config.tipo == TipoFila.PRIORIDADE:
                fila: FilaBase = FilaPrioridade(nome, config, fila_id)
            elif config.tipo == TipoFila.DEADLINE:
                fila = FilaDeadline(nome, config, fila_id)
            else:
                fila = FilaFIFO(nome, config, fila_id)
            if self._executor:
                fila.set_executor(self._executor)
            self._filas[fila_id] = fila
            return fila_id

    def adicionar_tarefa(
        self,
        fila_id: int,
        bloco: Bloco,
        prioridade: int = 5,
        deadline: Optional[float] = None,
        callback: Optional[Callable] = None,
    ) -> int:
        if fila_id not in self._filas:
            raise ValueError(f"Fila {fila_id} não existe")
        with self._lock:
            tarefa_id = self._proximo_tarefa_id
            self._proximo_tarefa_id += 1
        tarefa = Tarefa(
            id=tarefa_id,
            bloco=bloco,
            prioridade=prioridade,
            deadline=deadline,
            max_tentativas=self._filas[fila_id].config.max_retries,
            fila_id=fila_id,
            callback=callback,
        )
        self._filas[fila_id].adicionar(tarefa)
        self._filas[fila_id].iniciar()
        return tarefa_id

    def obter_resultado(self, tarefa_id: int) -> Any:
        for fila in self._filas.values():
            r = fila.obter_resultado(tarefa_id)
            if r is not None:
                return r
        return None

    def cancelar(self, tarefa_id: int) -> bool:
        for fila in self._filas.values():
            if fila.cancelar(tarefa_id):
                return True
        return False

    def get_status(self) -> Dict:
        return {
            "total_filas": len(self._filas),
            "filas": {fid: f.get_status() for fid, f in self._filas.items()},
        }


class MotorParallel:
    def __init__(self, nome: str = "MotorParallel"):
        self.nome = nome
        self._versao = "4.0.5-roko"
        self._inicializado = datetime.now()
        self.motor_decisao = MotorDecisao()
        self.executor = Executor(self)
        self.gerenciador_filas = GerenciadorFilas()
        self.gerenciador_filas.set_executor(self.executor)
        self._bloco_seq = 0
        self._lock = threading.Lock()

    def criar_fila(
        self, nome: str, tipo: str = "fifo", max_workers: int = 4, timeout: float = 30.0
    ) -> int:
        tipo_map = {
            "fifo": TipoFila.FIFO,
            "prioridade": TipoFila.PRIORIDADE,
            "priority": TipoFila.PRIORIDADE,
            "deadline": TipoFila.DEADLINE,
        }
        config = ConfiguracaoFila(
            tipo=tipo_map.get(tipo.lower(), TipoFila.FIFO),
            max_workers=min(max_workers, multiprocessing.cpu_count()),
            timeout=timeout,
        )
        return self.gerenciador_filas.criar_fila(nome, config)

    def submit(
        self,
        dados: List[Any],
        operacao: str,
        queue_id: Optional[int] = None,
        prioridade: int = 5,
        deadline: Optional[float] = None,
        nome: str = "",
    ) -> int:
        if queue_id is None:
            if 0 not in self.gerenciador_filas._filas:
                queue_id = self.criar_fila("default")
            else:
                queue_id = 0
        with self._lock:
            self._bloco_seq += 1
            bid = self._bloco_seq
        bloco = Bloco(
            id=bid,
            tipo=TipoBloco.FOR,
            dados=list(dados or []),
            operacao=operacao,
            nome=nome or f"op:{operacao}",
        )
        return self.gerenciador_filas.adicionar_tarefa(
            queue_id, bloco, prioridade=prioridade, deadline=deadline
        )

    def aguardar(self, task_id: int, timeout: Optional[float] = 30.0) -> Any:
        inicio = time.time()
        while True:
            if timeout and time.time() - inicio > timeout:
                raise TimeoutError(f"Tarefa {task_id} timeout")
            resultado = self.gerenciador_filas.obter_resultado(task_id)
            if resultado is not None:
                return resultado
            # check failure states roughly via status — simplified: just wait
            time.sleep(0.05)

    def execute(self, dados: List[Any], operacao: str) -> List[Any]:
        with self._lock:
            self._bloco_seq += 1
            bid = self._bloco_seq
        bloco = Bloco(id=bid, tipo=TipoBloco.FOR, dados=list(dados or []), operacao=operacao)
        estrategia = self.motor_decisao.decidir(bloco)
        return self.executor.executar_estrategia(bloco, estrategia)

    def cancel(self, task_id: int) -> bool:
        return self.gerenciador_filas.cancelar(task_id)

    def status(self, queue_id: Optional[int] = None) -> Dict:
        st = self.gerenciador_filas.get_status()
        if queue_id is not None:
            return st["filas"].get(queue_id, {"error": "queue not found"})
        return st

    def info(self) -> Dict:
        return {
            "nome": self.nome,
            "versao": self._versao,
            "cores": multiprocessing.cpu_count(),
            "filas": len(self.gerenciador_filas._filas),
            "stats_decisoes": self.motor_decisao._stats,
            "inicializado": self._inicializado.isoformat(),
        }

    def report(self) -> Dict:
        return {"status": "ok", "info": self.info(), "filas": self.status()}
