# `string.length`

**Categoria:** `string`  
**Descrição:** Tamanho da string

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_length`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.length WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/length.hmp`
