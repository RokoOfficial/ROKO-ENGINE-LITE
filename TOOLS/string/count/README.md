# `string.count`

**Categoria:** `string`  
**Descrição:** Conta ocorrências

## Parâmetros

`text`, `substring`

## Implementação

- `tool.py` — função `string_count`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET substring TO "ROKO"
CALL string.count WITH text=${text}, substring=${substring} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/count.hmp`
