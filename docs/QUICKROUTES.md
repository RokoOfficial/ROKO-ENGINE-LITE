# Quick Routes — ROKO ROUTER 2.1.0

## Rotas Rápidas

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/math/{operation}` | Operação matemática |
| POST | `/string/{operation}` | Operação string |
| POST | `/date/{operation}` | Operação date |
| POST | `/random/{operation}` | Operação random |
| POST | `/crypto/{operation}` | Operação crypto |

## Exemplos

### Math
```bash
curl -X POST /math/sum -d '{"a": 10, "b": 32}'
# → 42
```

### String
```bash
curl -X POST /string/upper -d '{"text": "hello"}'
# → HELLO
```

### Date
```bash
curl -X POST /date/now
# → 2026-08-20T12:00:00Z
```

### Random
```bash
curl -X POST /random/int -d '{"min": 1, "max": 100}'
# → 42
```

### Crypto
```bash
curl -X POST /crypto/hash -d '{"text": "hello", "algo": "sha256"}'
# → 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

## Status: ⏳ PENDING