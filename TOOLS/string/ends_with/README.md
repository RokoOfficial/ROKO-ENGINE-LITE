# `string.ends_with`

**Categoria:** `string`  
**Descrição:** Verifica sufixo

## Parâmetros

`text`, `suffix`

## Implementação

- `tool.py` — função `string_ends_with`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET suffix TO "!"
CALL string.ends_with WITH text=${text}, suffix=${suffix} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/ends_with.hmp`
