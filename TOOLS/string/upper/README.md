# `string.upper`

**Categoria:** `string`  
**Descrição:** Converte para maiúsculas

## Parâmetros

`text`

## Implementação

- `tool.py` — função `string_upper`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
CALL string.upper WITH text=${text} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/upper.hmp`
