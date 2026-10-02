# `json.parse`

**Categoria:** `json`  
**Descrição:** Converte JSON para objeto

## Parâmetros

`json_string`

## Implementação

- `tool.py` — função `json_parse`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET json_string TO "{\"ok\": true}"
CALL json.parse WITH json_string=${json_string} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/json/parse.hmp`
