# `http.status`

**Categoria:** `http`  
**Descrição:** Verifica status HTTP

## Parâmetros

`url`

## Implementação

- `tool.py` — função `http_status`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET url TO "https://httpbin.org/get"
CALL http.status WITH url=${url} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/http/status.hmp`
