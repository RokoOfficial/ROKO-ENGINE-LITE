# `list.merge`

**Categoria:** `list`  
**Descrição:** Funde duas listas

## Parâmetros

`list1`, `list2`

## Implementação

- `tool.py` — função `list_merge`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET list1 TO ""
SET list2 TO ""
CALL list.merge WITH list1=${list1}, list2=${list2} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/merge.hmp`
