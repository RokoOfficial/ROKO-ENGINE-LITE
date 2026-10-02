# `list.contains`

**Categoria:** `list`  
**Descrição:** Verifica se contém item

## Parâmetros

`items`, `value`

## Implementação

- `tool.py` — função `list_contains`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET value TO 42
CALL list.contains WITH items=${items}, value=${value} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/contains.hmp`
