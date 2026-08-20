# ROKO Script engine

ROKO Script is a compact workflow language used to sequence registered tools. The runtime parses the script into block statements, evaluates expressions through a restricted AST evaluator, and records execution data for synchronous results or streaming events.

## Statements

| Statement | Purpose | Example |
|---|---|---|
| `SET` | Store an evaluated value in a variable | `SET retries TO 3` |
| `CALL` | Invoke a registered tool | `CALL math.sum WITH a=7, b=8 AS total` |
| `RETURN` | End the script with a value | `RETURN total` |
| `IF` / `ELSE` / `END` | Conditional execution | `IF total > 10 THEN ... END` |
| `WHILE` / `END` | Loop while a condition remains true | `WHILE count < 3 DO ... END` |
| `FOR` / `END` | Iterate over an evaluated list-like value | `FOR item IN items DO ... END` |
| `BREAK` | Exit the innermost loop | `BREAK` |
| `CONTINUE` | Continue at the next loop iteration | `CONTINUE` |

Comments begin with `//` or `#`; blank lines are ignored. Block statements may use an inline body, such as `IF condition THEN RETURN value`, or a multiline body closed by `END`.

## Variables and interpolation

A variable reference can be embedded with `${name}`. Nested attributes and indexes can be resolved from variables and the most recent tool result.

```roko
SET user TO {"name": "Ada"}
SET items TO [2, 3, 5]
CALL list.get WITH items=${items}, index=0 AS first
CALL string.upper WITH text=${user.name} AS upper_name
RETURN {"first": first, "name": upper_name}
```

The `CALL` instruction accepts a literal tool name or a dynamic name resolved from a variable. It also supports passing a complete dictionary of parameters through interpolation.

```roko
SET selected_tool TO "math.sum"
SET params TO {"a": 7, "b": 8}
CALL ${selected_tool} WITH ${params} AS total
RETURN total
```

The supplied `ROKO_ROUTER.hmp` and `examples/semantic_router.roko` demonstrate this dynamic dispatch capability.

## Expressions

The evaluator accepts constants; list, tuple, and dictionary literals; arithmetic; comparison; boolean operators; variable names; and simple index or attribute access. Function calls are deliberately excluded from expressions. Invoke capabilities only through `CALL` so that all external behavior passes through the tool registry.

```roko
SET subtotal TO 18 + 3 * 2
SET eligible TO subtotal >= 20 and true
IF eligible THEN
    RETURN {"subtotal": subtotal, "eligible": eligible}
ELSE
    RETURN {"subtotal": subtotal, "eligible": eligible}
END
```

## Control flow example

```roko
SET values TO [1, 2, 3, 4]
SET total TO 0
FOR value IN values DO
    IF value == 3 THEN
        CONTINUE
    END
    SET total TO total + value
END
RETURN total
```

The parser tracks nested blocks and reports unmatched `END` or `ELSE` tokens, missing block closures, malformed conditions, and other syntax issues through `POST /script/validate` or the execution result.

## Execution results

A normal execution result includes the following information.

| Field | Meaning |
|---|---|
| `success` | Whether the interpreter completed without a controlled error |
| `output` | Collected output entries, when produced |
| `trace` | Ordered execution events |
| `variables` | Final variable state |
| `return_value` | Value supplied by `RETURN`, if any |
| `last_result` | Most recent tool result |
| `stats` | Runtime statistics, including tool calls and loop steps |
| `error` | Present when execution failed |

The stream endpoint uses the same event model. It emits a `start` event, sends individual trace items as `trace` events, and ends with a `done` event that carries the complete result. See [Streaming](SSE.md).

## Runtime limits

The runtime imposes fixed limits to bound parsing and loop behavior.

| Limit | Value |
|---|---:|
| Script lines | 10,000 |
| Block nesting depth | 64 |
| Iterations in one `WHILE` loop | 5,000 |
| Total loop steps across `FOR` and `WHILE` | 50,000 |
| Script execution time | 15 seconds |

These controls reduce accidental runaway execution, but they do not replace service-level authorization or resource isolation. A script may still reach whichever tools the server exposes. Review [Security](SECURITY.md) before accepting scripts from users with different trust levels.
