# `random.number`

**Categoria:** `random`  
**Descrição:** Número inteiro aleatório

## Parâmetros

`min_val`, `max_val`

## Implementação

- `tool.py` — função `random_number`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET min_val TO ""
SET max_val TO ""
CALL random.number WITH min_val=${min_val}, max_val=${max_val} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/random/number.hmp`
