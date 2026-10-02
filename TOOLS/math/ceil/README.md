# `math.ceil`

**Categoria:** `math`  
**Descrição:** Arredonda para cima

## Parâmetros

`a`

## Implementação

- `tool.py` — função `math_ceil`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
CALL math.ceil WITH a=${a} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/ceil.hmp`
