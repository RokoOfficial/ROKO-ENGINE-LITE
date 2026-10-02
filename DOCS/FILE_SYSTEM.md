# Script file management

The file API stores and executes `.roko` scripts from two locations created by `router.py`: `uploads/` for user-managed scripts and `examples/` for repository-provided samples. The project ships `examples/semantic_router.roko`, which is an executable copy of the dynamic-routing example provided in `ROKO_ROUTER.hmp`.

## Storage model

| Location | Created by | Read | Write through API | Delete through API | Run |
|---|---|---:|---:|---:|---:|
| `uploads/` | Runtime initialization | Yes | Yes | Yes | Yes |
| `examples/` | Runtime initialization / repository | Yes | No | No | Yes |

When looking up a script, the runtime checks `uploads/` before `examples/`. This means a user upload with the same sanitized name takes precedence for reads and runs; however, the upload endpoint refuses to create a name that already exists in `examples/`.

## Filename handling

The API accepts a filename, sanitizes it with Werkzeug's `secure_filename`, and appends `.roko` when absent. A blank filename after sanitization is rejected. File routes do not take arbitrary paths, so directory traversal strings cannot select files outside the managed directories.

| Input filename | Stored or resolved name |
|---|---|
| `workflow` | `workflow.roko` |
| `workflow.roko` | `workflow.roko` |
| `../../outside` | Sanitized name within the managed directory, with `.roko` appended |
| empty or unusable value | Rejected with HTTP `400` |

## API workflow

Create a script, inspect it, run it, change it, and remove it using the route sequence below.

```bash
# Create a user-managed script
curl -sS http://127.0.0.1:8989/files/upload \
  -H 'Content-Type: application/json' \
  -d '{
    "filename": "greeting",
    "content": "CALL string.upper WITH text=\"hello roko\" AS result\nRETURN result"
  }'

# Retrieve its content and metadata
curl -sS http://127.0.0.1:8989/files/greeting.roko

# Execute it with optional initial variables
curl -sS -X POST http://127.0.0.1:8989/files/run/greeting.roko \
  -H 'Content-Type: application/json' \
  -d '{"variables": {}, "debug": false}'

# Replace its content
curl -sS -X PUT http://127.0.0.1:8989/files/greeting.roko \
  -H 'Content-Type: application/json' \
  -d '{"content":"RETURN \"updated\""}'

# Remove the user upload
curl -sS -X DELETE http://127.0.0.1:8989/files/greeting.roko
```

## Responses and boundaries

| Operation | Success payload includes | Important failure cases |
|---|---|---|
| `GET /files` | `count`, file `name`, `size`, `source`, `created`, `modified` | Files that cannot be stat-ed are skipped |
| `POST /files/upload` | `success`, `filename`, byte `size`, `source: user` | Invalid filename `400`; example collision `409`; non-string content `400` |
| `GET /files/<name>` | `filename`, `content`, `source`, `size`, `modified` | Missing file `404` |
| `PUT /files/<name>` | `success`, `filename`, byte `size` | Example-only names and missing uploads cannot be updated |
| `DELETE /files/<name>` | `success`, confirmation message | Example-only names and missing uploads cannot be deleted |
| `POST /files/run/<name>` | Normal script result plus `filename` and `source` | Parser/runtime failure returns `400`; missing file returns `404` |

The request body limit applies to file API calls as well: the Quart application limits payloads to **2 MiB**. The current storage is local to the running process environment. Use a mounted volume, a managed object store integration, or another durable strategy if scripts must survive redeployments.
