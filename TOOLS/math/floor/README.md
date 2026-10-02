# `math.floor`

**Categoria:** `math`  
**Descrição:** Arredonda para baixo

## Parâmetros

`a`

## Implementação

- `tool.py` — função `math_floor`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
CALL math.floor WITH a=${a} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/floor.hmp`
