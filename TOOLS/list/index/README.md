# `list.index`

**Categoria:** `list`  
**Descrição:** Índice do item

## Parâmetros

`items`, `value`

## Implementação

- `tool.py` — função `list_index`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET value TO 42
CALL list.index WITH items=${items}, value=${value} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/index.hmp`
