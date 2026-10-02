# `log.error`

**Categoria:** `log`  
**Descrição:** Registra log ERROR

## Parâmetros

`message`

## Implementação

- `tool.py` — função `log_error`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET message TO "teste log"
CALL log.error WITH message=${message} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/log/error.hmp`
