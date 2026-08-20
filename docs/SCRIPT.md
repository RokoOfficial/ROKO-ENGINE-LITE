# Script Engine — ROKO ROUTER 2.1.0

## Visão Geral

O Script Engine processa arquivos `.roko` com comandos `CALL` e `RETURN`.

## Comandos

### CALL

```text
CALL math.sum(10, 32)
```

Executa uma tool registrada.

### RETURN

```text
RETURN last_result
```

Retorna o último resultado.

### Expressões

```text
CALL string.upper("hello")
RETURN last_result
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/script/execute` | Executa script |
| POST | `/script/validate` | Valida script |
| POST | `/script/stream` | Stream (SSE3) |

## Exemplo

```roko
CALL math.sum(10, 32)
CALL string.upper("resultado")
RETURN last_result
```

## Saída

```json
{
  "output": "RESULTADO",
  "return_value": "RESULTADO",
  "last_result": "RESULTADO",
  "trace": [
    {"tool": "math.sum", "result": 42.0},
    {"tool": "string.upper", "result": "RESULTADO"}
  ],
  "stats": {
    "tool_calls": 2,
    "loop_steps": 0
  }
}
```