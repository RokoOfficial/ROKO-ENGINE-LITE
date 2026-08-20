# Execução — ROKO ROUTER 2.1.0

## Pipeline de Execução

```text
┌──────────────────────────┐
│       EXECUTION          │
│                          │
│ 1. tool resolution       │
│ 2. parameter binding     │
│ 3. tool execution        │
│ 4. expression evaluation │
│ 5. error handling        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     OBSERVABILITY        │
│                          │
│ result                   │
│ return_value             │
│ last_result              │
│ output                   │
│ trace                    │
│ stats                    │
│ variables                │
│ tool_calls               │
│ loop_steps               │
└──────────────────────────┘
```

## Observabilidade

### Campos retornados

| Campo | Descrição |
|-------|-----------|
| `result` | Resultado final |
| `return_value` | Valor de retorno |
| `last_result` | Último resultado |
| `output` | Saída |
| `trace` | Rastreamento |
| `stats` | Estatísticas |
| `variables` | Variáveis |
| `tool_calls` | Chamadas de tools |
| `loop_steps` | Passos de loop |