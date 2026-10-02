# `list.filter`

**Categoria:** `list`  
**Descrição:** Filtra a lista

## Parâmetros

`items`, `condition`

## Implementação

- `tool.py` — função `list_filter`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET condition TO ""
CALL list.filter WITH items=${items}, condition=${condition} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/filter.hmp`
