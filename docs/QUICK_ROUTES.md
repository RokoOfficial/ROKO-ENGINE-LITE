# Quick Routes — ROKO ROUTER 2.1.0

## Visão Geral

Rotas rápidas para operações comuns sem precisar do Script Engine completo.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/math/{operation}` | Operação matemática |
| POST | `/string/{operation}` | Operação de string |
| POST | `/date/{operation}` | Operação de data |
| POST | `/random/{operation}` | Operação aleatória |
| POST | `/crypto/{operation}` | Operação criptográfica |

## Exemplos

### Math

```bash
curl -X POST /math/sum \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 32}'
```

```json
{"result": 42.0}
```

### String

```bash
curl -X POST /string/upper \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'
```

```json
{"result": "HELLO"}
```

### Date

```bash
curl -X POST /date/now
```

```json
{"result": "2026-08-20T12:00:00Z"}
```

### Random

```bash
curl -X POST /random/int \
  -H "Content-Type: application/json" \
  -d '{"min": 1, "max": 100}'
```

```json
{"result": 42}
```

### Crypto

```bash
curl -X POST /crypto/hash \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "algorithm": "sha256"}'
```

```json
{"result": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}
```

## Status

⏳ **PENDING** — Em desenvolvimento