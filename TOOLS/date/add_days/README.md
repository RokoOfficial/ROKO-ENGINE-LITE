# `date.add_days`

**Categoria:** `date`  
**Descrição:** Adiciona dias a uma data

## Parâmetros

`date_str`, `days`

## Implementação

- `tool.py` — função `date_add_days`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET date_str TO "2026-09-08"
SET days TO 3
CALL date.add_days WITH date_str=${date_str}, days=${days} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/date/add_days.hmp`
