# `http.get_json`

**Categoria:** `http`  
**Descrição:** HTTP GET com retorno JSON

## Parâmetros

`url`, `headers`

## Implementação

- `tool.py` — função `http_get_json`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET url TO "https://httpbin.org/get"
SET headers TO {}
CALL http.get_json WITH url=${url}, headers=${headers} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/http/get_json.hmp`
