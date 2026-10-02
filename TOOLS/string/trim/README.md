# `string.trim`

**Categoria:** `string`  
**Descrição:** Remove espaços em branco

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_trim`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.trim WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/trim.hmp`
