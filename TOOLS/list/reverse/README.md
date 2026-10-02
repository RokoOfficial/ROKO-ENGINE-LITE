# `list.reverse`

**Categoria:** `list`  
**Descrição:** Inverte a lista

## Parâmetros

`items`

## Implementação

- `tool.py` — função `list_reverse`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
CALL list.reverse WITH items=${items} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/reverse.hmp`
