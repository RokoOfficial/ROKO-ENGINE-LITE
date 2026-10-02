# `string.reverse`

**Categoria:** `string`  
**Descrição:** Inverte a string

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_reverse`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.reverse WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/reverse.hmp`
