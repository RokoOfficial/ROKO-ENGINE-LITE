# `list.unique`

**Categoria:** `list`  
**Descrição:** Remove duplicatas

## Parâmetros

`items`

## Implementação

- `tool.py` — função `list_unique`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
CALL list.unique WITH items=${items} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/unique.hmp`
