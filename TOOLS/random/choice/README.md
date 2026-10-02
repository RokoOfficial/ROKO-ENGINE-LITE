# `random.choice`

**Categoria:** `random`  
**Descrição:** Escolhe item aleatório

## Parâmetros

`items`

## Implementação

- `tool.py` — função `random_choice`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
CALL random.choice WITH items=${items} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/random/choice.hmp`
