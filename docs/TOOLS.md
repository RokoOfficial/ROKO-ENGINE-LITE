# Tools and registry

The tool registry is defined in `tools.py`. Each native tool is represented by metadata containing its callable implementation, category, description, and parameter names. The metadata powers API discovery, category listings, help, search, generic execution, and dynamic `CALL` dispatch from ROKO Script.

The runtime currently exposes **92 tools**: 87 native tool specifications plus 5 metadata tools.

| Category | Native tools | Examples |
|---|---:|---|
| `math` | 15 | `math.sum`, `math.factorial`, `math.average` |
| `string` | 19 | `string.upper`, `string.replace`, `string.pad_right` |
| `list` | 17 | `list.append`, `list.unique`, `list.sort_numeric` |
| `json` | 4 | `json.parse`, `json.get`, `json.set` |
| `date` | 7 | `date.now`, `date.add_days`, `date.diff_days` |
| `http` | 6 | `http.get`, `http.post`, `http.status` |
| `crypto` | 5 | `crypto.uuid`, `crypto.hash`, `crypto.random_string`, `crypto.md5`, `crypto.sha1` |
| `random` | 5 | `random.number`, `random.choice`, `random.boolean` |
| `log` | 4 | `log.print`, `log.warning`, `log.error` |
| `system` | 5 | `system.env`, `system.version`, `system.platform` |
| `meta` | 5 | `meta.tools`, `meta.categories`, `meta.help`, `meta.info`, `meta.search` |

> The exposed count is generated from the registry at runtime. Query `GET /tools` or `GET /tools/categories` rather than relying on this page when integrating against a running service.

## Discovery

Use the HTTP API to enumerate and filter the registry.

```bash
# Full metadata registry
curl -sS http://127.0.0.1:8989/tools

# Category view
curl -sS http://127.0.0.1:8989/tools/category/math

# Text search across names, descriptions, and parameter names
curl -sS 'http://127.0.0.1:8989/tools/search?q=hash'

# Detailed metadata for one tool
curl -sS http://127.0.0.1:8989/tools/help/math.sum
```

`GET /tools` also accepts optional `category` and `search` query parameters. When both appear, the API applies both filters to the metadata collection.

## Tool execution

The generic execution endpoint receives a JSON object whose keys match the tool's declared parameters.

```bash
curl -sS http://127.0.0.1:8989/tool/string.replace \
  -H 'Content-Type: application/json' \
  -d '{"text":"ROKO lite","old":"lite","new":"ENGINE"}'
```

Tool calls return the following envelope.

| Field | Meaning |
|---|---|
| `tool` | Tool name requested by the client |
| `success` | Whether parameter binding and execution completed |
| `result` | Native tool result when successful |
| `error` | Failure explanation when unsuccessful |

The same tools are available inside ROKO Script with `CALL`.

```roko
CALL crypto.uuid WITH AS id
CALL string.upper WITH text="roko" AS upper
RETURN {"id": id, "upper": upper}
```

## Metadata tools

Metadata tools are callable from scripts and available through the generic execution endpoint.

| Tool | Required input | Result |
|---|---|---|
| `meta.tools` | None | All registry metadata |
| `meta.categories` | None | Category-to-tool mapping |
| `meta.help` | `tool_name` | Metadata for one tool |
| `meta.info` | None | Runtime and registry summary |
| `meta.search` | `query` | Matching tools based on names, descriptions, and parameters |

The sample router uses `meta.search` to collect candidates and then invokes a dynamically selected tool. Search ranking is based on normalized substring and word overlap; results should not be interpreted as semantic similarity scores.

## Extension rules

A new tool should be added as a static method on `RokoTools` and registered in `TOOL_SPECS` with a category, a concise description, and parameter names that mirror the function signature. Keep the implementation independent of the HTTP and parser layers, then validate all of the following:

| Check | Why it matters |
|---|---|
| Import `tools.py` independently | Maintains the lowest-layer boundary |
| Inspect `GET /tools/help/<tool>` | Confirms discovery metadata is useful |
| Invoke `POST /tool/<tool>` | Confirms parameter binding and error handling |
| Call the tool from a script | Confirms dynamic interpreter dispatch |
| Review quick-route maps | Adds a shortcut only when the operation fits an existing family |

Tools that read the environment, access the network, or write logs carry operational implications. They should be disabled, filtered, or protected according to the deployment's trust model.
