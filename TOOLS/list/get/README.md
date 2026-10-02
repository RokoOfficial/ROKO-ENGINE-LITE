# `list.get`

**Categoria:** `list`  
**Descrição:** Obtém item por índice

## Parâmetros

`items`, `index`

## Implementação

- `tool.py` — função `list_get`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET index TO 0
CALL list.get WITH items=${items}, index=${index} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/get.hmp`
