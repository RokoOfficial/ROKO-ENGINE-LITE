# `string.contains`

**Categoria:** `string`  
**Descrição:** Verifica se contém substring

## Parâmetros

`text`, `substring`

## Implementação

- `tool.py` — função `string_contains`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET substring TO "ROKO"
CALL string.contains WITH text=${text}, substring=${substring} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/contains.hmp`
