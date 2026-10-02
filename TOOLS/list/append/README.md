# `list.append`

**Categoria:** `list`  
**Descrição:** Adiciona item ao final

## Parâmetros

`items`, `item`

## Implementação

- `tool.py` — função `list_append`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET item TO 99
CALL list.append WITH items=${items}, item=${item} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/append.hmp`
