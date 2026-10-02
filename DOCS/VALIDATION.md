# Validation — 2.3.1

## Bateria executada (2026-09-12)

```text
PYTHONPATH=. python tests/test_battery.py
→ 41 passed, 0 failed
```

Cobertura:

- Registry / meta (versão, contagens, native vs roko)
- Tools core: math, string, list, json, crypto, date, system
- Script engine: SET, CALL, IF, WHILE, RETURN, variáveis
- Prioridade Oracle vs native
- agent.run (plan math_demo → soma 15, dobro 30)
- HGR: store_fact, get_fact, search_facts, stats
- HTTP: status + get_json (fix requests)
- parallel.info + meta.info
- Plans e presença Oracle (≥100 .roko)
- Limits: MAX_EXEC_SECONDS=60

## Smoke

```bash
PYTHONPATH=. python tests/smoke_test.py
```

## Correções aplicadas nesta release

1. `TOOLS/http/get_json/tool.py` — requests directo
2. `TOOLS/system/version/tool.py` — APP_VERSION/TOOL_VERSION
3. `engine/limits.py` — MAX_EXEC_SECONDS = 60
4. Docs e versão 2.3.1 alinhadas
