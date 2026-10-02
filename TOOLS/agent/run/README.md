# agent.run

Loop agentic **simbólico** (ROKO→ROKO, sem LLM).

## Uso

```roko
CALL agent.run WITH
  plan="plans/math_demo.roko",
  goal="Somar 7 e 8 e mostrar o dobro",
  max_steps=4,
  user_id="ada",
  id="demo-1"
AS result
RETURN result
```

## Parâmetros

| Campo | Obrigatório | Default |
|-------|-------------|---------|
| plan | sim | — |
| goal | sim | — |
| id | não | gerado |
| max_steps | não | 8 |
| user_id | não | default |
| vars | não | {} |

O `plan` pode ser path relativo à raiz (`plans/...`, `Oracle/...`) ou script inline.
