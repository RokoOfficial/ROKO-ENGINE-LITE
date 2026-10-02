# `random.shuffle`

**Categoria:** `random`  
**Descrição:** Embaralha lista

## Parâmetros

`items`

## Implementação

- `tool.py` — função `random_shuffle`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
CALL random.shuffle WITH items=${items} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/random/shuffle.hmp`
