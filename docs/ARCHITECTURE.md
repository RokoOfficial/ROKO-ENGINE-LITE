# Architecture

## Overview

ROKO ENGINE LITE separates transport concerns from runtime behavior. The HTTP layer does not parse or execute scripts directly; it delegates to a small facade, which in turn connects the interpreter to the registered tools. This layout keeps tool implementations independent of Quart and allows the script runtime to be embedded or tested without starting the web service.

```text
Client
  │
  ├── REST request ─────────────────────────────────────────────────────┐
  │                                                                      ▼
  │                                                            api.py (Quart)
  │                                                              │      │
  │                                                              │      └── SSE responses
  │                                                              ▼
  │                                                        router.py
  │                                                        │       │
  │                                          file helpers  │       └── application metadata
  │                                                        ▼
  │                                                     roko.py
  │                                              parser + interpreter
  │                                                        │
  └──────────────────────────────────────────────────────────────────────▼
                                                               tools.py
                                                     registry + native implementations
```

| Module | Boundary | Main responsibilities |
|---|---|---|
| `api.py` | HTTP transport | Routes, JSON validation, HTTP status selection, CORS, SSE streaming, request/response logging |
| `router.py` | Application facade | Version and safety constants, script wrappers, tool-discovery wrappers, `.roko` path handling |
| `roko.py` | Language runtime | Restricted-expression evaluation, block parsing, statement dispatch, traces, statistics, event callbacks |
| `tools.py` | Tool boundary | Native implementations, declarative metadata, category construction, metadata search, parameter binding |
| `main.py` | Process entry | Imports the Quart application and starts it with environment configuration |

## Request-to-result flow

For a synchronous script request, `api.py` checks that a non-empty script and object-shaped variables were provided. `router.run_script()` creates a `RokoInterpreter`, which parses the source into statements, evaluates them in order, and delegates each `CALL` to `tools.execute_tool()`. The final JSON result is returned to the client with HTTP `200` when `success` is true and `400` when execution failed.

The streaming route follows the same execution path but supplies an event callback. The interpreter runs in a worker thread and publishes execution events to an asynchronous queue. The HTTP layer exposes that queue as Server-Sent Events, emitting `start`, zero or more `trace`, and one terminal `done` event. See [Streaming](SSE.md) for the wire format.

## Script storage

The facade initializes four directories next to the Python modules when it is imported.

| Directory | Purpose | API behavior |
|---|---|---|
| `uploads/` | User-managed `.roko` scripts | Writable through the file endpoints |
| `examples/` | Repository-provided `.roko` scripts | Readable and runnable, but protected from overwrite through the API |
| `logs/` | Output produced by logging tools | Created on demand by the runtime |
| `temp/` | Runtime scratch location | Created by the application facade |

`find_roko_file()` checks `uploads/` first and then `examples/`. File names are sanitized with Werkzeug's `secure_filename`, and a missing `.roko` extension is appended. File names are not path selectors: callers cannot choose an arbitrary filesystem path through the file routes.

## Data and error boundaries

The API uses a uniform application-error shape: `{"success": false, "error": "..."}`. Tool execution returns a structured result that is wrapped with the requested tool name on `POST /tool/<tool_name>`. Script execution includes the interpreter state—such as output, trace, variables, return value, and statistics—when available.

The runtime restricts expression syntax through an AST allowlist and directs function-like behavior through the registered `CALL` mechanism. That is a language-level control, not a complete deployment boundary. Tools such as the HTTP and environment utilities can still expose meaningful capabilities to scripts; deployment should therefore apply authentication, authorization, rate limits, egress controls, and an allowlist appropriate to the intended audience. See [Security](SECURITY.md).

## Extending the runtime

Add a native tool in `RokoTools`, define its metadata in `TOOL_SPECS`, and keep its implementation free of imports from `roko.py` and `api.py`. The registry metadata drives listing, categories, search, help, the generic execution endpoint, and dynamic `CALL` dispatch. Changes to the public tool surface should be accompanied by updates to [Tools](TOOLS.md), [Quick routes](QUICK_ROUTES.md) when relevant, and the [API reference](API.md).
