# `string.title`

**Categoria:** `string`  
**Descrição:** Converte para formato título

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_title`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.title WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/title.hmp`
