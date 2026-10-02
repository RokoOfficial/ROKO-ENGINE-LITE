# `json.get`

**Categoria:** `json`  
**Descrição:** Obtém valor por chave

## Parâmetros

`obj`, `key`, `default`

## Implementação

- `tool.py` — função `json_get`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET obj TO {"x": 1, "y": 2}
SET key TO "x"
SET default TO null
CALL json.get WITH obj=${obj}, key=${key}, default=${default} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/json/get.hmp`
