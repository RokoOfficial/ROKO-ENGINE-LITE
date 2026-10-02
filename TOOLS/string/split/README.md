# `string.split`

**Categoria:** `string`  
**Descrição:** Divide string em lista

## Parâmetros

`text`, `separator`

## Implementação

- `tool.py` — função `string_split`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET separator TO " "
CALL string.split WITH text=${text}, separator=${separator} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/split.hmp`
