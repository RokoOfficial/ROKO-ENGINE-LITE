# `string.starts_with`

**Categoria:** `string`  
**Descrição:** Verifica prefixo

## Parâmetros

`text`, `prefix`

## Implementação

- `tool.py` — função `string_starts_with`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET prefix TO "He"
CALL string.starts_with WITH text=${text}, prefix=${prefix} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/starts_with.hmp`
