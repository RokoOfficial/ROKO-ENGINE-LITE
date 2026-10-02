# `math.average`

**Categoria:** `math`  
**Descrição:** Calcula a média aritmética

## Parâmetros

`args...`

## Implementação

- `tool.py` — função `math_average`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET args... TO ""
CALL math.average WITH args...=${args...} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/average.hmp`
