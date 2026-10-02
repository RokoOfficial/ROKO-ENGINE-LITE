# `crypto.hash`

**Categoria:** `crypto`  
**Descrição:** Gera hash SHA-256

## Parâmetros

`text`

## Implementação

- `tool.py` — função `crypto_hash`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL crypto.hash WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/crypto/hash.hmp`
