# `string.replace`

**Categoria:** `string`  
**Descrição:** Substitui texto

## Parâmetros

`text`, `old`, `new`

## Implementação

- `tool.py` — função `string_replace`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET old TO "o"
SET new TO "0"
CALL string.replace WITH text=${text}, old=${old}, new=${new} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/replace.hmp`
