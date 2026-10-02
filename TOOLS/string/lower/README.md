# `string.lower`

**Categoria:** `string`  
**Descrição:** Converte para minúsculas

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_lower`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.lower WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/lower.hmp`
