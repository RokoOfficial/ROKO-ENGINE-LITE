# `string.slice`

**Categoria:** `string`  
**Descrição:** Fatiamento de string

## Parâmetros

`text`, `start`, `end`

## Implementação

- `tool.py` — função `string_slice`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET start TO 0
SET end TO 5
CALL string.slice WITH text=${text}, start=${start}, end=${end} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/slice.hmp`
