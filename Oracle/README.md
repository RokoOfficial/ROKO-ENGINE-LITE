# Oracle — Tools em idioma ROKO (`.roko`)

Cada ficheiro `Oracle/<categoria>/<nome>.roko` é uma **tool executável**.

## Layout

```text
Oracle/
  math/sum.roko          → CALL math.sum
  http/status.roko       → CALL http.status
  memory/store_fact.roko → CALL memory.store_fact
  ...
  demos/                 → legados .hmp (não registados como tools)
  README.md
```

## Metadados

```roko
// @name: math.sum
// @category: math
// @description: Soma dois números
// @params: a, b

RETURN ${a} + ${b}
```

## Tipos

1. **Pura ROKO** — só expressões / IF / RETURN (ex.: `math.sum`)
2. **Wrapper** — `CALL native.<tool> ...` e `RETURN` (HTTP, crypto, etc.)

## Prioridade no registry

- `CALL math.sum` → Oracle `.roko` (se existir)
- `CALL native.math.sum` → implementação Python em `TOOLS/`

## Demos

Ficheiros em `Oracle/demos/` (antigos `.hmp`) **não** são carregados como tools.
