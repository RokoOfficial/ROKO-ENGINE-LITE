# Runtime Engine — ROKO ROUTER 2.1.0

## Operações

| Operação | Descrição |
|----------|-----------|
| `CALL` | Executa tool |
| `RETURN` | Retorna valor |
| `EXPRESSIONS` | Avalia expressões |
| `VARIABLES` | Gerencia variáveis |
| `TRACE` | Rastreamento |
| `STATS` | Estatísticas |

## Pipeline

```text
┌──────────────────┐
│   RUNTIME ENGINE │
│                  │
│ CALL             │
│ RETURN           │
│ EXPRESSIONS      │
│ VARIABLES        │
│ TRACE            │
│ STATS            │
└──────────────────┘
```

## Integração

- **Tool Registry** → resolução de tools
- **Tool Runtime** → execução
- **Execution** → pipeline completo
- **Observability** → métricas e rastreamento

## Exemplo

```text
CALL math.sum(10, 32)
```

**Trace:**

```json
{
  "tool_calls": 1,
  "loop_steps": 0,
  "result": 42.0,
  "success": true
}
```