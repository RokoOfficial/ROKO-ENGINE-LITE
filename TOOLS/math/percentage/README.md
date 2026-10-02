# `math.percentage`

**Categoria:** `math`  
**Descrição:** Calcula a porcentagem

## Parâmetros

`value`, `total`

## Implementação

- `tool.py` — função `math_percentage`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET value TO 42
SET total TO ""
CALL math.percentage WITH value=${value}, total=${total} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/math/percentage.hmp`
