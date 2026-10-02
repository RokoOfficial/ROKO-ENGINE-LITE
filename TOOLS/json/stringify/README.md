# `json.stringify`

**Categoria:** `json`  
**Descrição:** Converte objeto para JSON

## Parâmetros

`obj`

## Implementação

- `tool.py` — função `json_stringify`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET obj TO {"x": 1, "y": 2}
CALL json.stringify WITH obj=${obj} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/json/stringify.hmp`
