# `math.min`

**Categoria:** `math`  
**Descrição:** Retorna o menor valor

## Parâmetros

`args...`

## Implementação

- `tool.py` — função `math_min`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET args... TO ""
CALL math.min WITH args...=${args...} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/min.hmp`
