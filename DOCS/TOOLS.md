# Tools

## Duas fontes

| Fonte | Path | Nome no CALL |
|-------|------|----------------|
| Oracle (prioridade) | `Oracle/<cat>/<name>.roko` | `cat.name` |
| Python | `TOOLS/<cat>/<name>/` | `native.cat.name` (e fallback) |

## Discovery

1. Carrega todas as tools Python → regista `nome` e `native.nome`
2. Carrega `Oracle/**/*.roko` (ignora `demos/`) → sobrescreve o nome público

## Criar uma tool Oracle

```roko
// @name: math.triple
// @category: math
// @description: Multiplica por 3
// @params: x

RETURN ${x} * 3
```

Gravar em `Oracle/math/triple.roko`. Reiniciar processo ou `reload_tools()`.

## Meta tools

- `meta.tools`, `meta.categories`, `meta.help`, `meta.info`, `meta.search`

## Agent

- `agent.run` — loop simbólico (plan + goal + HGR)

## Contagem actual (2.3.1)

- **121** tools Oracle (`.roko`)
- **5** meta
- **126** total público
- Natives Python disponíveis via `native.*`

Categorias: agent, auth, cron, crypto, date, http, json, list, log, math, memory, meta, parallel, random, string, system.

## Testes

```bash
PYTHONPATH=. python tests/test_battery.py
```

Valida math, string, list, json, crypto, date, system, script (IF/WHILE), agent.run, HGR, http, parallel, limites.
