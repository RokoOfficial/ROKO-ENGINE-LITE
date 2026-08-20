# Exemplos — ROKO ROUTER 2.1.0

## Tool Execution

### math.sum

```bash
curl -X POST /tool/math.sum \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 32}'
```

```json
{
  "result": 42.0,
  "success": true,
  "tool": "math.sum"
}
```

### string.upper

```bash
curl -X POST /tool/string.upper \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
```

```json
{
  "result": "HELLO WORLD",
  "success": true,
  "tool": "string.upper"
}
```

### list.length

```bash
curl -X POST /tool/list.length \
  -H "Content-Type: application/json" \
  -d '{"list": [1, 2, 3, 4, 5]}'
```

```json
{
  "result": 5,
  "success": true,
  "tool": "list.length"
}
```

## Script Engine

### Script simples

```roko
CALL math.sum(10, 32)
RETURN last_result
```

```bash
curl -X POST /script/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "CALL math.sum(10, 32)\nRETURN last_result"}'
```

```json
{
  "output": 42.0,
  "return_value": 42.0,
  "last_result": 42.0,
  "trace": [
    {"tool": "math.sum", "result": 42.0}
  ],
  "stats": {
    "tool_calls": 1,
    "loop_steps": 0
  }
}
```

### Múltiplas chamadas

```roko
CALL math.sum(10, 32)
CALL string.upper("resultado")
RETURN last_result
```

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

## Erros

### Tool inválida

```json
{
  "error": "Tool not found: invalid.tool",
  "success": false
}
```

### Parâmetro faltando

```json
{
  "error": "Missing parameter: a",
  "success": false
}
```

### Erro de runtime

```json
{
  "error": "Division by zero",
  "success": false
}
```