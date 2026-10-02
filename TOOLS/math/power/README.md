# `math.power`

**Categoria:** `math`  
**Descrição:** Eleva à potência

## Parâmetros

`a`, `b`

## Implementação

- `tool.py` — função `math_power`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
SET b TO 8
CALL math.power WITH a=${a}, b=${b} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/power.hmp`
