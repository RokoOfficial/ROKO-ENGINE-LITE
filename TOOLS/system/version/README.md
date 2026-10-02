# `system.version`

**Categoria:** `system`  
**Descrição:** Versão do sistema

## Parâmetros

_(nenhum)_

## Implementação

- `tool.py` — função `system_version`
- `spec.py` — metadados para o registry

## Exemplo ROKO Script

```roko

CALL system.version AS resultado
RETURN {"resultado": resultado}
```

## Oracle

Script de demonstração: `Oracle/system/version.hmp`
