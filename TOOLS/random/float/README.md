# `random.float`

**Categoria:** `random`  
**Descrição:** Número decimal aleatório

## Parâmetros

`min_val`, `max_val`

## Implementação

- `tool.py` — função `random_float`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET min_val TO ""
SET max_val TO ""
CALL random.float WITH min_val=${min_val}, max_val=${max_val} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/random/float.hmp`
