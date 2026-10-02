# `http.delete`

**Categoria:** `http`  
**Descrição:** Requisição HTTP DELETE

## Parâmetros

`url`, `headers`

## Implementação

- `tool.py` — função `http_delete`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET url TO "https://httpbin.org/get"
SET headers TO {}
CALL http.delete WITH url=${url}, headers=${headers} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/http/delete.hmp`
