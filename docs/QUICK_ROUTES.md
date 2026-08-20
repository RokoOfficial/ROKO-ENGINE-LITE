# Quick routes

Quick routes provide concise HTTP access to common tool families. They accept either query-string parameters with `GET` or a JSON object with `POST`, select a friendly operation alias, invoke the mapped tool, and return a compact response containing `operation`, `tool`, and `result`.

```bash
curl -sS 'http://127.0.0.1:8989/math/sum?a=10&b=5'
curl -sS -X POST http://127.0.0.1:8989/string/upper \
  -H 'Content-Type: application/json' \
  -d '{"text":"roko"}'
```

When the same parameter is supplied in the query string and in the JSON body, the query-string value is used. Unsupported operation aliases and tool-level failures return HTTP `400`.

## Math

| Route operation | Registered tool |
|---|---|
| `sum`, `add` | `math.sum` |
| `subtract`, `sub` | `math.subtract` |
| `multiply`, `mul` | `math.multiply` |
| `divide`, `div` | `math.divide` |
| `power`, `pow` | `math.power` |
| `sqrt` | `math.sqrt` |
| `abs` | `math.abs` |
| `floor` | `math.floor` |
| `ceil` | `math.ceil` |
| `round` | `math.round` |
| `factorial` | `math.factorial` |
| `percentage` | `math.percentage` |
| `average` | `math.average` |

Accepted quick-route fields are `a`, `b`, `n`, `value`, and `decimals`.

## String

| Route operation | Registered tool |
|---|---|
| `upper`, `lower`, `capitalize`, `title`, `reverse` | Matching `string.*` tool |
| `length`, `len` | `string.length` |
| `trim`, `replace`, `split`, `join`, `contains` | Matching `string.*` tool |
| `starts_with`, `ends_with`, `find`, `slice` | Matching `string.*` tool |
| `append`, `count`, `pad_left`, `pad_right` | Matching `string.*` tool |

Accepted quick-route fields are `text`, `old`, `new`, `substring`, `prefix`, `suffix`, `length`, and `char`.

## Date

| Route operation | Registered tool |
|---|---|
| `now` | `date.now` |
| `timestamp` | `date.timestamp` |
| `format` | `date.format` |
| `add_days` | `date.add_days` |
| `add_hours` | `date.add_hours` |
| `diff_days` | `date.diff_days` |
| `parse` | `date.parse` |

Accepted quick-route fields are `date_str`, `format_str`, `days`, `hours`, `date1`, and `date2`.

## Random and crypto

| Family | Route operation | Registered tool |
|---|---|---|
| Random | `number`, `int` | `random.number` |
| Random | `float`, `choice`, `shuffle` | Matching `random.*` tool |
| Random | `boolean`, `bool` | `random.boolean` |
| Crypto | `uuid`, `hash`, `md5`, `sha1`, `random_string` | Matching `crypto.*` tool |

The random family accepts `min_val`, `max_val`, `items`, and `length`. The crypto family accepts `text` and `length`.

## Response contract

A successful quick route returns a compact form rather than the full generic tool envelope.

```json
{
  "operation": "sum",
  "tool": "math.sum",
  "result": 15.0
}
```

The route accepts only the parameter names listed for its family. For uncommon tools, metadata inspection, or access to every registered parameter, use `POST /tool/<tool_name>` instead.
