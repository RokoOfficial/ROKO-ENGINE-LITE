# `list.set`

**Categoria:** `list`  
**Descrição:** Define item por índice

## Parâmetros

`items`, `index`, `value`

## Implementação

- `tool.py` — função `list_set`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET index TO 0
SET value TO 42
CALL list.set WITH items=${items}, index=${index}, value=${value} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/set.hmp`
