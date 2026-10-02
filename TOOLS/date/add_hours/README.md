# `date.add_hours`

**Categoria:** `date`  
**Descrição:** Adiciona horas a uma data

## Parâmetros

`date_str`, `hours`

## Implementação

- `tool.py` — função `date_add_hours`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET date_str TO "2026-09-08"
SET hours TO 2
CALL date.add_hours WITH date_str=${date_str}, hours=${hours} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/date/add_hours.hmp`
