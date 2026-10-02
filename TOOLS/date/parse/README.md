# `date.parse`

**Categoria:** `date`  
**Descrição:** Parseia data em múltiplos formatos

## Parâmetros

`date_str`

## Implementação

- `tool.py` — função `date_parse`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET date_str TO "2026-09-08"
CALL date.parse WITH date_str=${date_str} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/date/parse.hmp`
