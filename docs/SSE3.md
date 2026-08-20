# SSE3 — Server-Sent Events

## Status: 🔄 STANDBY

## Endpoint

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/script/stream` | Stream de execução em tempo real |

## Funcionalidades Planejadas

- [ ] Streaming de execução de scripts
- [ ] Eventos em tempo real
- [ ] Progresso de execução
- [ ] Resultados parciais
- [ ] Cancelamento de execução

## Formato do Evento

```json
{
  "type": "progress",
  "data": {
    "step": 1,
    "total": 10,
    "message": "Executando...",
    "timestamp": "2026-08-20T12:00:00Z"
  }
}
```

## Tipos de Evento

| Tipo | Descrição |
|------|-----------|
| `start` | Início da execução |
| `progress` | Progresso parcial |
| `tool_call` | Chamada de tool |
| `result` | Resultado parcial |
| `complete` | Execução completa |
| `error` | Erro na execução |

## Uso

```bash
curl -N -X POST /script/stream \
  -H "Content-Type: application/json" \
  -d '{"script": "CALL math.sum(10, 32)"}'
```

## Estado: 🔄 STANDBY