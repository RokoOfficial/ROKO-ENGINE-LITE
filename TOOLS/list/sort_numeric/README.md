# `list.sort_numeric`

**Categoria:** `list`  
**Descrição:** Ordena numericamente

## Parâmetros

`items`, `reverse`

## Implementação

- `tool.py` — função `list_sort_numeric`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET reverse TO false
CALL list.sort_numeric WITH items=${items}, reverse=${reverse} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/sort_numeric.hmp`
