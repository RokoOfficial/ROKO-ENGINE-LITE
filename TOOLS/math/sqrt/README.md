# `math.sqrt`

**Categoria:** `math`  
**Descrição:** Raiz quadrada

## Parâmetros

`a`

## Implementação

- `tool.py` — função `math_sqrt`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET a TO 7
CALL math.sqrt WITH a=${a} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/sqrt.hmp`
