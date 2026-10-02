# `math.subtract`

**Categoria:** `math`  
**Descrição:** Subtrai dois números

## Parâmetros

`a`, `b`

## Implementação

- `tool.py` — função `math_subtract`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
SET b TO 8
CALL math.subtract WITH a=${a}, b=${b} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/subtract.hmp`
