# `log.debug`

**Categoria:** `log`  
**Descrição:** Registra log DEBUG

## Parâmetros

`message`

## Implementação

- `tool.py` — função `log_debug`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET message TO "teste log"
CALL log.debug WITH message=${message} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/log/debug.hmp`
