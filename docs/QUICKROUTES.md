# Quick Routes — ROKO ROUTER 2.1.0

## Rotas Rápidas

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/math/{operation}` | Operação matemática rápida |
| POST | `/string/{operation}` | Operação de string rápida |
| POST | `/date/{operation}` | Operação de data rápida |
| POST | `/random/{operation}` | Operação aleatória rápida |
| POST | `/crypto/{operation}` | Operação criptográfica rápida |

## Exemplos

### Math

```bash
curl -X POST http://localhost:8000/math/sum \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 32}'
```

### String

```bash
curl -X POST http://localhost:8000/string/upper \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'
```

### Date

```bash
curl -X POST http://localhost:8000/date/now
```

### Random

```bash
curl -X POST http://localhost:8000/random/int \
  -H "Content-Type: application/json" \
  -d '{"min": 1, "max": 100}'
```

### Crypto

```bash
curl -X POST http://localhost:8000/crypto/hash \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "algorithm": "sha256"}'
```

## Status: ⏳ PENDING