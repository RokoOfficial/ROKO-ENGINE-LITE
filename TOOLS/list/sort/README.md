# `list.sort`

**Categoria:** `list`  
**Descrição:** Ordena a lista

## Parâmetros

`items`, `reverse`

## Implementação

- `tool.py` — função `list_sort`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET reverse TO false
CALL list.sort WITH items=${items}, reverse=${reverse} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/sort.hmp`
