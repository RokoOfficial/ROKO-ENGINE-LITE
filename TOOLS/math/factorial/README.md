# `math.factorial`

**Categoria:** `math`  
**Descrição:** Fatorial de um número

## Parâmetros

`n`

## Implementação

- `tool.py` — função `math_factorial`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET n TO 5
CALL math.factorial WITH n=${n} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/factorial.hmp`
