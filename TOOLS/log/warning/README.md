# `log.warning`

**Categoria:** `log`  
**Descrição:** Registra log WARNING

## Parâmetros

`message`

## Implementação

- `tool.py` — função `log_warning`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET message TO "teste log"
CALL log.warning WITH message=${message} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/log/warning.hmp`
