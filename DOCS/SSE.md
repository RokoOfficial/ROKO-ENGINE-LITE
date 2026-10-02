# Server-Sent Events streaming

`POST /script/stream` executes a ROKO Script and streams its execution lifecycle through **Server-Sent Events (SSE)**. It accepts the same JSON request shape as `POST /script/execute` but responds with `Content-Type: text/event-stream` rather than a single JSON result.

The interpreter itself is synchronous. The API runs it in a worker thread, forwards callback events into an asynchronous queue, and yields each queue item as it arrives. This produces incremental trace events during execution instead of returning the complete trace only after the script finishes.

## Request

```bash
curl -N -X POST http://127.0.0.1:8989/script/stream \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d '{
    "script": "SET a TO 7\nSET b TO 8\nCALL math.sum WITH a=${a}, b=${b} AS total\nRETURN total",
    "variables": {},
    "debug": false
  }'
```

The request fields are:

| Field | Required | Type | Meaning |
|---|---:|---|---|
| `script` | Yes | string | Non-empty ROKO Script source |
| `variables` | No | object | Initial variable map; defaults to `{}` |
| `debug` | No | boolean | Enables detailed unexpected-error information in the runtime result |

A missing or blank script, or a non-object `variables` value, returns the normal JSON error response with HTTP `400` before the stream is opened.

## Event sequence

| Event name | Occurrence | Data payload |
|---|---|---|
| `start` | Exactly once before execution begins | `{"script_lines": <integer>}` |
| `trace` | Zero or more times during execution | One interpreter event, such as `set`, `call`, `if`, loop lifecycle, `return`, `break`, `continue`, `expr`, or `error` |
| `done` | Exactly once after execution terminates | The complete result shape returned by `/script/execute` |

A typical stream is formatted as follows.

```text
event: start
data: {"script_lines":4}

event: trace
data: {"type":"set","...":"..."}

event: trace
data: {"type":"call","...":"..."}

event: done
data: {"success":true,"return_value":15.0,"...":"..."}
```

The response sets `Cache-Control: no-cache` and `X-Accel-Buffering: no` to discourage intermediary buffering. Reverse proxies must still be configured to preserve streaming behavior and to use timeouts that accommodate the runtime's maximum execution duration.

## Browser client

The browser's `EventSource` API only opens GET requests, while this endpoint uses POST with a JSON body. Use `fetch()` and read the response stream instead.

```javascript
const response = await fetch('/script/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
  body: JSON.stringify({
    script: 'CALL math.sum WITH a=7, b=8 AS total\nRETURN total',
    variables: {}
  })
});

const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
let buffer = '';

while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  buffer += value;
  const blocks = buffer.split('\n\n');
  buffer = blocks.pop();

  for (const block of blocks) {
    const event = block.match(/^event: (.+)$/m)?.[1];
    const data = block.match(/^data: (.+)$/m)?.[1];
    if (event && data) console.log(event, JSON.parse(data));
  }
}
```

Treat the `done` event as authoritative for final success or failure. Individual trace events are observability data and may include an `error` event before the terminal result is sent.
