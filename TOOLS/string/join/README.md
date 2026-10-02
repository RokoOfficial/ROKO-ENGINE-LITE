# `string.join`

**Categoria:** `string`  
**Descrição:** Junta lista em string

## Parâmetros

`items`, `separator`

## Implementação

- `tool.py` — função `string_join`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
SET separator TO " "
CALL string.join WITH items=${items}, separator=${separator} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/join.hmp`
