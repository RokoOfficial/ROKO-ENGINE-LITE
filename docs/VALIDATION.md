# Validation guide

This document defines the release checks for the modular ROKO ENGINE LITE runtime. It distinguishes static verification, deterministic runtime checks, HTTP-route checks, and the supplied dynamic-router example. Run the checks in an isolated environment with the project's declared dependencies installed.

## Validation matrix

| Layer | Check | Expected outcome |
|---|---|---|
| Syntax | Compile `api.py`, `router.py`, `roko.py`, `tools.py`, and `main.py` | No compilation error |
| Tool registry | Inspect categories and invoke `math.sum` | Registry metadata is available and the result is `15.0` for `7 + 8` |
| Script runtime | Execute `SET`, `CALL`, and `RETURN` | Successful result with the expected return value |
| Dynamic dispatch | Run the semantic-router example | A candidate is selected and invoked through `CALL ${variable}` |
| Validation endpoint | Submit a valid and an invalid block script | Valid source is accepted; malformed source returns parser errors without tool execution |
| HTTP API | Exercise `/`, `/health`, `/tools`, `/tool`, `/script/execute`, `/files`, and quick routes | Route-specific success payloads and expected status codes |
| SSE | Consume `/script/stream` | `start`, trace events, and `done` in order |
| File controls | Upload, read, run, update, and delete a user script | User scripts work in `uploads/`; examples remain protected |

## Static check

```bash
python -m py_compile api.py router.py roko.py tools.py main.py
```

## Runtime smoke checks

The repository includes a smoke test that exercises the tool registry, a simple script, the dynamic-routing sample, core HTTP routes, and the streaming route. It uses only local deterministic tools.

```bash
python tests/smoke_test.py
```

The dynamic router is intentionally a keyword-overlap demo. The included test confirms that its bundled `soma` sample selects `math.sum`; it does not claim embedding-style semantic precision. Add focused tests alongside this smoke test whenever new public behavior is introduced.

## HTTP checks

Start the server in one terminal, then use a separate terminal for the requests.

```bash
python main.py
```

```bash
curl -fsS http://127.0.0.1:8989/health
curl -fsS http://127.0.0.1:8989/tools/categories
curl -fsS -X POST http://127.0.0.1:8989/tool/math.sum \
  -H 'Content-Type: application/json' \
  -d '{"a":7,"b":8}'
curl -fsS -X POST http://127.0.0.1:8989/script/validate \
  -H 'Content-Type: application/json' \
  -d '{"script":"IF true THEN\nRETURN 1\nEND"}'
curl -N -X POST http://127.0.0.1:8989/script/stream \
  -H 'Content-Type: application/json' \
  -d '{"script":"RETURN 1"}'
```

## Release acceptance

A release is ready to publish only when syntax compilation passes, deterministic tool and script checks pass, core routes respond with their documented status behavior, and the security configuration has been reviewed for the target environment. Add targeted regression checks whenever a public route, language statement, registry tool, or persistence behavior changes.
