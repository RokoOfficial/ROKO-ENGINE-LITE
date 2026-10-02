# `list.remove_at`

**Categoria:** `list`  
**Descrição:** Remove item por índice

## Parâmetros

`items`, `index`

## Implementação

- `tool.py` — função `list_remove_at`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET index TO 0
CALL list.remove_at WITH items=${items}, index=${index} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/remove_at.hmp`
