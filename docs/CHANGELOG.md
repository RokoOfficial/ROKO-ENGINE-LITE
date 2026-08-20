# Changelog

All notable project changes are recorded in this file.

## [2.1.0] - 2026-08-20

### Added

| Area | Change |
|---|---|
| Modular runtime | Added `api.py`, `router.py`, `roko.py`, and `tools.py` as distinct layers for transport, orchestration, interpretation, and tool execution |
| Script language | Added multiline block parsing for `IF` / `ELSE`, `WHILE`, and `FOR`; `BREAK`; `CONTINUE`; safe expression evaluation; and execution traces |
| Dynamic dispatch | Added support for dynamic tool names and parameter dictionaries in `CALL` instructions |
| Streaming | Added real-time Server-Sent Event delivery from interpreter callbacks through `POST /script/stream` |
| File API | Added managed `.roko` listing, upload, read, update, delete, and run routes |
| Quick routes | Added common math, string, date, random, and crypto operation shortcuts |
| Example | Added `ROKO_ROUTER.hmp` and executable `examples/semantic_router.roko` dynamic-routing samples |
| Documentation | Replaced outdated documents with an English documentation set aligned to the modular implementation |

### Changed

| Area | Change |
|---|---|
| Entry point | `main.py` now imports and launches the same Quart application exposed by `api.py` |
| Dependencies | Replaced the unused `sse-starlette` requirement with `requests` and `werkzeug`, which are used by the modular tool and file layers |
| API behavior | Health, tool, script, file, quick-route, and streaming endpoints are now implemented by the public application entry point |
| Runtime controls | Added explicit script line, block-depth, loop-step, and execution-time limits |

### Compatibility notes

The previous repository entry point exposed only three service-information routes. The new `main.py` retains its role as the startup command but now serves the modular API on port `8989` by default. Existing deployments that relied on port `8000` must set `PORT=8000` explicitly.

The sample semantic router performs lexical metadata matching. It should not be described as vector search or embedding-based semantic routing.

## [2.0.0] - 2026-07-15

### Added

- Initial lightweight router structure.
- Basic service-information endpoints.

## [1.0.0] - 2026-06-01

### Added

- Initial project foundation.
