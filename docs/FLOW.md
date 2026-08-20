# Fluxos de Execução — ROKO ROUTER 2.1.0

## Fluxo de uma Tool

```text
Cliente
   │
   │ POST /tool/math.sum
   │ { "a": 10, "b": 32 }
   ▼
ROKO ROUTER
   │
   ▼
Tool Registry
   │
   │ resolve: math.sum
   ▼
Runtime
   │
   │ math_sum(10, 32)
   ▼
Resultado
   │
   ├── result = 42.0
   ├── success = true
   └── tool = math.sum
   ▼
Cliente
```

## Fluxo de um .roko

```text
POST /files/upload
        │
        ▼
   arquivo.roko
        │
        ▼
   Storage / Files
        │
        │ POST /files/run/{filename}
        ▼
   Runtime Engine
        │
        ├── parse
        ├── expression
        ├── CALL
        ├── RETURN
        │
        ▼
   Execution Trace
        │
        ├── output
        ├── return_value
        ├── last_result
        ├── stats
        └── variables
        │
        ▼
      Cliente
```

## Fluxo conceitual do Script Engine

```text
SCRIPT
   │
   ▼
┌───────────────┐
│     PARSER    │
└───────┬───────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
EXPRESSÃO  CALL
   │         │
   ▼         ▼
 literal   Tool Registry
   │         │
   │         ▼
   │     Tool Runtime
   │         │
   │         ▼
   │      resultado
   │         │
   └────┬────┘
        ▼
   last_result
        │
        ▼
      RETURN
        │
        ▼
   return_value
```