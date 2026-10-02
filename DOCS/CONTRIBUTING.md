# Contributing

Contributions are welcome when they preserve the modular design and document any public behavior changes. Before opening a pull request, describe the problem being solved, keep the change focused, and avoid bundling unrelated refactors with feature work.

## Development expectations

| Area | Expectation |
|---|---|
| Module boundaries | Keep HTTP behavior in `api.py`, application coordination in `router.py`, language behavior in `roko.py`, and native tools in `tools.py` |
| Tool additions | Add implementation, registry metadata, discovery coverage, and script-level verification |
| Public API changes | Update `docs/API.md` and any affected quick-route, file, streaming, or security documentation |
| Language changes | Update `docs/SCRIPT_ENGINE.md` and add a regression check |
| Security-sensitive changes | Document operational implications in `docs/SECURITY.md` and avoid exposing secrets in tests or examples |
| Examples | Keep them deterministic, local, and safe to run in a development environment |

## Local checks

Install the project requirements and run the versioned smoke test before submitting a change.

```bash
python -m pip install -r requirements.txt
python -m py_compile api.py router.py roko.py tools.py main.py tests/smoke_test.py
python tests/smoke_test.py
```

The smoke test covers the registry, a basic script, the dynamic-router sample, several HTTP routes, and the streaming endpoint. Add targeted tests when a change affects error handling, parsing, control flow, parameter binding, storage, or route semantics.

## Pull request guidance

A pull request should explain the user-visible change, list validation performed, identify affected documentation, and note any compatibility or deployment implications. Avoid adding a dependency unless it is necessary and declared in `requirements.txt`.
