# `string.pad_right`

**Categoria:** `string`  
**Descrição:** Preenche à direita

## Parâmetros

`text`, `length`, `char`

## Implementação

- `tool.py` — função `string_pad_right`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko
SET text TO "Hello ROKO"
SET length TO 10
SET char TO "*"
CALL string.pad_right WITH text=${text}, length=${length}, char=${char} AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/string/pad_right.hmp`
