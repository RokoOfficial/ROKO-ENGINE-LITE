# `http.put`

**Categoria:** `http`  
**Descrição:** Requisição HTTP PUT

## Parâmetros

`url`, `data`, `headers`

## Implementação

- `tool.py` — função `http_put`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET url TO "https://httpbin.org/get"
SET data TO {"ping": 1}
SET headers TO {}
CALL http.put WITH url=${url}, data=${data}, headers=${headers} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/http/put.hmp`
