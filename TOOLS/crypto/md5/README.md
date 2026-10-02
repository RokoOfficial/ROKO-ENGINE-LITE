# `crypto.md5`

**Categoria:** `crypto`  
**Descrição:** Gera hash MD5

## Parâmetros

`text`

## Implementação

- `tool.py` — função `crypto_md5`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL crypto.md5 WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/crypto/md5.hmp`
