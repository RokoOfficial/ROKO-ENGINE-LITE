# `date.diff_days`

**Categoria:** `date`  
**Descrição:** Diferença em dias entre duas datas

## Parâmetros

`date1`, `date2`

## Implementação

- `tool.py` — função `date_diff_days`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET date1 TO "2026-01-01"
SET date2 TO "2026-09-08"
CALL date.diff_days WITH date1=${date1}, date2=${date2} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/date/diff_days.hmp`
