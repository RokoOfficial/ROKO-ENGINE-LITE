# ROKO ENGINE LITE

**ROKO ENGINE LITE** is a lightweight automation runtime that packages the modular **ROKO Router** implementation. It exposes a Quart-based HTTP API, a registry of built-in tools, and a small interpreted language for composing tool calls into controlled workflows.

The runtime is organized so that the language engine, the tool registry, the application facade, and the HTTP layer remain independently understandable and testable. The included `ROKO_ROUTER.hmp` artifact demonstrates a rule-based tool-selection workflow that selects and invokes a registered tool at runtime.

> The router sample uses keyword overlap against tool metadata. It is not an embedding-based or vector-search semantic engine.

| Component | Responsibility | Primary file |
|---|---|---|
| HTTP API | REST endpoints, CORS, Server-Sent Events, errors | `api.py` |
| Application facade | Configuration, script and file helpers | `router.py` |
| Script runtime | Parser, safe expression evaluation, control flow | `roko.py` |
| Tool registry | Native tools, metadata, search, invocation | `tools.py` |
| Entry point | Backward-compatible server launcher | `main.py` |

## Quick start

The project requires **Python 3.10 or later**. Create an isolated environment, install the dependencies, and start the API with either supported entry point.

```bash
git clone https://github.com/RokoOfficial/ROKO-ENGINE-LITE.git
cd ROKO-ENGINE-LITE
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

By default, the service listens on `0.0.0.0:8989`. The port, host, debug mode, and application secret can be configured through environment variables.

```bash
HOST=127.0.0.1 PORT=8989 ROKO_DEBUG=false ROKO_SECRET_KEY='replace-me' python main.py
curl http://127.0.0.1:8989/health
```

A healthy instance responds with a JSON payload containing `status`, `timestamp`, and the application version.

## API at a glance

| Area | Primary endpoint | Purpose |
|---|---|---|
| Service information | `GET /` | API map, versions, tool and category counts |
| Tool discovery | `GET /tools` | List, filter, search, and inspect registered tools |
| Tool execution | `POST /tool/<tool_name>` | Invoke one tool with a JSON object |
| Script execution | `POST /script/execute` | Execute a ROKO Script and return its complete result |
| Script streaming | `POST /script/stream` | Stream execution events as Server-Sent Events |
| Script validation | `POST /script/validate` | Parse a script without executing tools |
| Script files | `GET/POST/PUT/DELETE /files...` | Manage `.roko` files and run stored scripts |
| Quick operations | `/math`, `/string`, `/date`, `/random`, `/crypto` | Map common operations to registered tools |

For request schemas, response shapes, and working examples, see the [API reference](docs/API.md).

## ROKO Script example

The following script assigns values, invokes a registered tool, and returns the captured result.

```roko
SET a TO 7
SET b TO 8
CALL math.sum WITH a=${a}, b=${b} AS total
RETURN {"total": total}
```

Submit it through the API.

```bash
curl -sS http://127.0.0.1:8989/script/execute \
  -H 'Content-Type: application/json' \
  -d '{"script":"SET a TO 7\nSET b TO 8\nCALL math.sum WITH a=${a}, b=${b} AS total\nRETURN {\"total\": total}"}'
```

The interpreter supports `SET`, `CALL`, `RETURN`, `IF` / `ELSE`, `FOR`, `WHILE`, `BREAK`, and `CONTINUE`. Expressions are parsed through a restricted Python AST; function calls are not accepted in expressions, and tool invocation is intentionally limited to the `CALL` instruction. Read the [script-engine guide](docs/SCRIPT_ENGINE.md) before exposing user-authored scripts to an untrusted audience.

## Documentation

| Document | Coverage |
|---|---|
| [Architecture](docs/ARCHITECTURE.md) | Module boundaries, runtime flow, and storage locations |
| [Installation](docs/INSTALLATION.md) | Local setup, configuration, and production process guidance |
| [API reference](docs/API.md) | HTTP endpoints, payloads, and status behavior |
| [Script engine](docs/SCRIPT_ENGINE.md) | Grammar, interpolation, limits, and execution results |
| [Tools](docs/TOOLS.md) | Tool categories, metadata, discovery, and invocation |
| [File system](docs/FILE_SYSTEM.md) | `.roko` upload, retrieval, update, deletion, and execution |
| [Quick routes](docs/QUICK_ROUTES.md) | Shortcut operation maps and request conventions |
| [Streaming](docs/SSE.md) | Server-Sent Event lifecycle and client example |
| [Security](docs/SECURITY.md) | Deployment boundaries and hardening considerations |
| [Validation](docs/VALIDATION.md) | Release verification scope and reproducible checks |
| [Changelog](docs/CHANGELOG.md) | Versioned project changes |

## Repository layout

```text
.
├── api.py                 # Quart routes and SSE response generation
├── router.py              # Application facade and `.roko` storage helpers
├── roko.py                # Parser and interpreter
├── tools.py               # Tool implementations and metadata registry
├── main.py                # Compatible server entry point
├── ROKO_ROUTER.hmp        # Rule-based dynamic-routing sample
├── examples/
│   └── semantic_router.roko
├── docs/
└── requirements.txt
```

## License and contributions

The repository does not currently include a license file. Add an explicit license before distributing or reusing the code under defined terms. Contributions should preserve the modular boundaries described in [the architecture guide](docs/ARCHITECTURE.md) and should update the relevant documentation when they alter public behavior.
