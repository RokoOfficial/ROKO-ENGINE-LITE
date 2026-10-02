# `string.find`

**Categoria:** `string`  
**Descrição:** Encontra posição da substring

## Parâmetros

`text`, `substring`

## Implementação

- `tool.py` — função `string_find`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET substring TO "ROKO"
CALL string.find WITH text=${text}, substring=${substring} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/find.hmp`
