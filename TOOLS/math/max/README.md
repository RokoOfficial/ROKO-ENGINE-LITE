# `math.max`

**Categoria:** `math`  
**Descrição:** Retorna o maior valor

## Parâmetros

`args...`

## Implementação

- `tool.py` — função `math_max`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET args... TO ""
CALL math.max WITH args...=${args...} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/max.hmp`
