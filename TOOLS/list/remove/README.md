# `list.remove`

**Categoria:** `list`  
**Descrição:** Remove item da lista

## Parâmetros

`items`, `item`

## Implementação

- `tool.py` — função `list_remove`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET item TO 99
CALL list.remove WITH items=${items}, item=${item} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/remove.hmp`
