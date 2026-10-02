# `date.format`

**Categoria:** `date`  
**Descrição:** Formata data

## Parâmetros

`date_str`, `format_str`

## Implementação

- `tool.py` — função `date_format`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET date_str TO "2026-09-08"
SET format_str TO "%Y-%m-%d"
CALL date.format WITH date_str=${date_str}, format_str=${format_str} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/date/format.hmp`
