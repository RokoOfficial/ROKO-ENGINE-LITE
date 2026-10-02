# `math.round`

**Categoria:** `math`  
**Descrição:** Arredonda para n casas decimais

## Parâmetros

`a`, `decimals`

## Implementação

- `tool.py` — função `math_round`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
SET decimals TO 2
CALL math.round WITH a=${a}, decimals=${decimals} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/round.hmp`
