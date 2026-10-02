# `string.capitalize`

**Categoria:** `string`  
**Descrição:** Capitaliza a string

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_capitalize`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.capitalize WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/capitalize.hmp`
