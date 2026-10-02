# `crypto.sha1`

**Categoria:** `crypto`  
**Descrição:** Gera hash SHA-1

## Parâmetros

`text`

## Implementação

- `tool.py` — função `crypto_sha1`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL crypto.sha1 WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/crypto/sha1.hmp`
