# Script Engine — ROKO ROUTER 2.1.0

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/script/execute` | Executa script |
| POST | `/script/validate` | Valida script |
| POST | `/script/stream` | Stream (SSE3) |

## Comandos

### CALL

```text
CALL math.sum(10, 32)
```

### RETURN

```text
RETURN last_result
```

### EXPRESSIONS

```text
x = 10 + 32
```

### VARIABLES

```text
SET x = 42
```

## Fluxo

```text
SCRIPT
   │
   ▼
PARSER
   │
   ├── EXPRESSÃO → valor literal
   └── CALL → Tool Registry → Tool Runtime → resultado
   │
   ▼
last_result
   │
   ▼
RETURN
   │
   ▼
return_value
```

## Exemplo

```text
CALL math.sum(10, 32)
RETURN last_result
```

**Resultado:** `42.0`