# ROKO ENGINE LITE

**Version 2.3.1** — A modular automation runtime with an HTTP API (Quart), a tool registry, the **ROKO Script** language, **HGR** memory, a symbolic **ROKO→ROKO** agent (without an LLM), and Oracle tools written in `.roko`.

## Highlights

- **126 tools**: 121 Oracle `.roko` tools and 5 meta tools, with Python implementations under `TOOLS/`.
- **Oracle `.roko`**: `CALL x.y` prioritizes Oracle implementations; `native.x.y` explicitly selects Python.
- **Symbolic agent**: `agent.run` supports plans, goals, step limits, and HGR persistence.
- **HGR v5**: step status, parallel groups, batched recording, and a facade API.
- **Parallel engine**: queue-based parallel execution.
- **Execution limits**: a 60-second maximum and recursion protection for `.roko` tools.

## Quick start

```bash
cd ROKO_ENGINE_LITE
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The API listens on `0.0.0.0:8989` by default.

## Example

```roko
CALL math.sum WITH a=3, b=4 AS s
CALL string.lower WITH text="ROKO" AS t
RETURN {"s": ${s}, "t": ${t}}
```

See [`Oracle/README.md`](Oracle/README.md) and [`DOCS/TOOLS.md`](DOCS/TOOLS.md) for the tool model and resolution rules.

## Symbolic agent

The runtime executes `.roko` plans without an LLM and records steps in HGR:

```roko
CALL agent.run WITH
  plan="plans/math_demo.roko",
  goal="Add 7 and 8, then double the result",
  max_steps=4,
  user_id="demo-user",
  id="demo-1"
AS result
RETURN result
```

## Tests

```bash
PYTHONPATH=. python tests/smoke_test.py
PYTHONPATH=. python tests/test_battery.py
```

## Documentation

- [`DOCS/ARCHITECTURE.md`](DOCS/ARCHITECTURE.md) — layers, flows, and diagrams
- [`DOCS/TOOLS.md`](DOCS/TOOLS.md) — Oracle/native catalog and priority
- [`DOCS/SCRIPT_ENGINE.md`](DOCS/SCRIPT_ENGINE.md) — ROKO Script language
- [`DOCS/API.md`](DOCS/API.md) — HTTP endpoints
- [`DOCS/SECURITY.md`](DOCS/SECURITY.md) — operational security guidance
- [`DOCS/CHANGELOG.md`](DOCS/CHANGELOG.md) — release history

## License and attribution

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

Copyright 2026 openroko/noka.
