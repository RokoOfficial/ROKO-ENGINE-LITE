# HTTP API reference

The service returns JSON for normal endpoints and `text/event-stream` for `POST /script/stream`. Application errors use the shape `{"success": false, "error": "message"}`. Tool and script requests expect `Content-Type: application/json` when they carry a body.

## Service information

| Method | Route | Success response |
|---|---|---|
| `GET` | `/` | Service name, application and API versions, status, tool/category counts, and an endpoint map |
| `GET` | `/health` | `status`, ISO-8601 `timestamp`, and application version |
| `GET` | `/version` | Application, API, tool, Python, and platform versions |

```bash
curl -sS http://127.0.0.1:8989/health
```

## Tool discovery and execution

| Method | Route | Parameters or body | Behavior |
|---|---|---|---|
| `GET` | `/tools` | Optional `category`, optional `search` | Lists registry metadata, optionally applying both filters |
| `GET` | `/tools/categories` | None | Returns category names and their tools |
| `GET` | `/tools/category/<category>` | Path category | Returns the tools belonging to one category; `404` if absent |
| `GET` | `/tools/search?q=<query>` | Required `q` | Searches names, descriptions, and parameter names; `400` if `q` is empty |
| `GET` | `/tools/help/<tool_name>` | Path tool name | Returns metadata or a not-found detail for the selected tool |
| `POST` | `/tool/<tool_name>` | JSON parameters object | Executes one registered or metadata tool |

Execute a single tool by sending the parameters named by its metadata.

```bash
curl -sS http://127.0.0.1:8989/tool/math.sum \
  -H 'Content-Type: application/json' \
  -d '{"a": 7, "b": 8}'
```

A successful invocation includes the requested `tool` name, `success: true`, and the `result`. Invalid parameters, unknown tools, and tool-level failures are returned with `success: false` and HTTP `400`.

## Script routes

| Method | Route | Request JSON | Behavior |
|---|---|---|---|
| `POST` | `/script/execute` | `script` string; optional `variables` object; optional `debug` boolean | Executes the entire script and returns the final interpreter result |
| `POST` | `/script/stream` | Same as execute | Streams runtime events using Server-Sent Events |
| `POST` | `/script/validate` | `script` string | Parses syntax only; no tool is called |

Execute a short script:

```bash
curl -sS http://127.0.0.1:8989/script/execute \
  -H 'Content-Type: application/json' \
  -d '{
    "script": "SET value TO 6\nCALL math.factorial WITH n=${value} AS result\nRETURN result",
    "variables": {},
    "debug": false
  }'
```

The execution result normally contains `success`, `output`, `trace`, `variables`, `return_value`, `last_result`, and `stats`. On a controlled runtime failure, the result also contains `error`; the endpoint responds with HTTP `400`.

```bash
curl -sS http://127.0.0.1:8989/script/validate \
  -H 'Content-Type: application/json' \
  -d '{"script":"IF true THEN\n  RETURN 1\nEND"}'
```

Validation returns `valid`, `errors`, and `line_count`. It confirms that the parser accepts the script structure but does not prove that every runtime tool call will succeed.

## Script file routes

The file API manages `.roko` files in the runtime's `uploads/` directory. Repository examples are listed and runnable but cannot be overwritten through these routes.

| Method | Route | Request JSON | Behavior |
|---|---|---|---|
| `GET` | `/files` | None | Lists user uploads and repository examples |
| `POST` | `/files/upload` | `filename`, `content` string | Creates or replaces a user script after filename sanitization |
| `GET` | `/files/<filename>` | None | Reads a user upload or an example |
| `PUT` | `/files/<filename>` | `content` string | Updates an existing user upload |
| `DELETE` | `/files/<filename>` | None | Deletes an existing user upload |
| `POST` | `/files/run/<filename>` | Optional `variables` object and `debug` boolean | Runs a user upload or an example |

```bash
curl -sS http://127.0.0.1:8989/files/upload \
  -H 'Content-Type: application/json' \
  -d '{"filename":"hello","content":"CALL string.upper WITH text=\"hello\" AS result\nRETURN result"}'

curl -sS -X POST http://127.0.0.1:8989/files/run/hello.roko \
  -H 'Content-Type: application/json' \
  -d '{"variables": {}}'
```

A filename without the `.roko` suffix receives it automatically. The maximum request payload is **2 MiB**; larger requests receive HTTP `413`.

## Quick routes

Quick routes accept either query-string parameters on `GET` or a JSON object on `POST`. Each route maps a friendly operation name to a registered tool. The full operation maps and parameter conventions are documented in [Quick routes](QUICK_ROUTES.md).

| Method | Route family | Example |
|---|---|---|
| `GET`, `POST` | `/math/<operation>` | `/math/sum?a=10&b=5` |
| `GET`, `POST` | `/string/<operation>` | `/string/upper?text=roko` |
| `GET`, `POST` | `/date/<operation>` | `/date/now` |
| `GET`, `POST` | `/random/<operation>` | `/random/number?min_val=1&max_val=10` |
| `GET`, `POST` | `/crypto/<operation>` | `/crypto/uuid` |

## Status behavior

| HTTP status | Meaning |
|---:|---|
| `200` | Request completed successfully |
| `400` | Invalid request, missing required input, unknown quick operation, or controlled tool/script failure |
| `404` | Unknown route, unknown category, or unavailable script file |
| `405` | The route exists but does not accept the request method |
| `409` | Attempt to overwrite a repository example through the upload endpoint |
| `413` | Request payload exceeds 2 MiB |
| `500` | Unhandled server-side failure; details are exposed only in debug mode |

The application enables CORS for all origins in the current source. Treat the API as a trusted-network service until this policy is narrowed and access controls are installed.
