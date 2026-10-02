# `http.get`

**Categoria:** `http`  
**Descrição:** Requisição HTTP GET

## Parâmetros

`url`, `headers`

## Implementação

- `tool.py` — função `http_get`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET url TO "https://httpbin.org/get"
SET headers TO {}
CALL http.get WITH url=${url}, headers=${headers} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/http/get.hmp`
