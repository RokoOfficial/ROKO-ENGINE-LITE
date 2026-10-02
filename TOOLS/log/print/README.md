# `log.print`

**Categoria:** `log`  
**Descrição:** Registra log INFO

## Parâmetros

`message`, `level`

## Implementação

- `tool.py` — função `log_print`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET message TO "teste log"
SET level TO "info"
CALL log.print WITH message=${message}, level=${level} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/log/print.hmp`
