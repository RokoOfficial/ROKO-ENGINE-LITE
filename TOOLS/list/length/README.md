# `list.length`

**Categoria:** `list`  
**Descrição:** Tamanho da lista

## Parâmetros

`items`

## Implementação

- `tool.py` — função `list_length`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET items TO [1, 2, 3]
CALL list.length WITH items=${items} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/list/length.hmp`
