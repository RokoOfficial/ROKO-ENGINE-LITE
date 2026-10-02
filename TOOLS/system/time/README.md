# `system.time`

**Categoria:** `system`  
**Descrição:** Hora atual

## Parâmetros

_(nenhum)_

## Implementação

- `tool.py` — função `system_time`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko

CALL system.time AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/system/time.hmp`
