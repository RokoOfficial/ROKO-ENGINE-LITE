# `list.slice`

**Categoria:** `list`  
**Descrição:** Fatiamento de lista

## Parâmetros

`items`, `start`, `end`

## Implementação

- `tool.py` — função `list_slice`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET start TO 0
SET end TO 5
CALL list.slice WITH items=${items}, start=${start}, end=${end} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/slice.hmp`
