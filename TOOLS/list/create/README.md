# `list.create`

**Categoria:** `list`  
**Descrição:** Cria uma lista

## Parâmetros

`items...`

## Implementação

- `tool.py` — função `list_create`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items... TO ""
CALL list.create WITH items...=${items...} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/create.hmp`
