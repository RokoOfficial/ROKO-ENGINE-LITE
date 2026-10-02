# `crypto.random_string`

**Categoria:** `crypto`  
**Descrição:** Gera string aleatória

## Parâmetros

`length`

## Implementação

- `tool.py` — função `crypto_random_string`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET length TO 10
CALL crypto.random_string WITH length=${length} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/crypto/random_string.hmp`
