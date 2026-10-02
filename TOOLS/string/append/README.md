# `string.append`

**Categoria:** `string`  
**Descrição:** Concatena strings

## Parâmetros

`text`, `suffix`

## Implementação

- `tool.py` — função `string_append`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET suffix TO "!"
CALL string.append WITH text=${text}, suffix=${suffix} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/append.hmp`
