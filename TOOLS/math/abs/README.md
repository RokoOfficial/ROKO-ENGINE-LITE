# `math.abs`

**Categoria:** `math`  
**Descrição:** Valor absoluto

## Parâmetros

`a`

## Implementação

- `tool.py` — função `math_abs`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
CALL math.abs WITH a=${a} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/abs.hmp`
