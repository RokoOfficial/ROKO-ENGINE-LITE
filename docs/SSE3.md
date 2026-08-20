# SSE3 — Server-Sent Events — ROKO ROUTER 2.1.0

## Visão Geral

SSE3 permite streaming em tempo real de execução de scripts.

## Endpoint

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/script/stream` | Stream de execução |

## Fluxo

```text
Cliente ──POST /script/stream──▶ ROKO ROUTER
    ▲                              │
    │                              ▼
    │                         Runtime Engine
    │                              │
    │                              ▼
    │                         Event Stream
    │                              │
    └──────────SSE Events──────────┘
```

## Eventos

| Evento | Descrição |
|--------|-----------|
| `start` | Início da execução |
| `tool_call` | Chamada de tool |
| `result` | Resultado parcial |
| `end` | Fim da execução |
| `error` | Erro durante execução |

## Exemplo

```bash
curl -N -X POST /script/stream \
  -H "Content-Type: application/json" \
  -d '{"script": "CALL math.sum(10, 32)\\nRETURN last_result"}'
```

## Resposta SSE

```text
event: start
data: {"status": "running"}

event: tool_call
data: {"tool": "math.sum", "params": {"a": 10, "b": 32}}

event: result
data: {"result": 42.0}

event: end
data: {"status": "completed", "return_value": 42.0}
```

## Status

🔄 **STANDBY** — Pronto para implementação