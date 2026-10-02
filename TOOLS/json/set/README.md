# `json.set`

**Categoria:** `json`  
**Descrição:** Define valor por chave

## Parâmetros

`obj`, `key`, `value`

## Implementação

- `tool.py` — função `json_set`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET obj TO {"x": 1, "y": 2}
SET key TO "x"
SET value TO 42
CALL json.set WITH obj=${obj}, key=${key}, value=${value} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/json/set.hmp`
