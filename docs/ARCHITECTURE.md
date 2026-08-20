# ROKO ROUTER 2.1.0 — Arquitetura

## Visão Geral

```text
┌──────────────────────────┐
│       CLIENT / APP       │
│   curl / Web / Agent     │
└────────────┬─────────────┘
             │
             ▼
┌────────────────────────────────┐
│        ROKO ROUTER 2.1.0       │
│          Quart + CORS           │
│              + SSE               │
└───────────────┬────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌──────────┐ ┌─────────┐
│API INFO│ │TOOL SYS  │ │ SCRIPT  │
│GET /   │ │GET /tools│ │/execute │
│/health │ │/search   │ │/validate│
│/version│ │/category │ │/stream  │
└────────┘ └────┬─────┘ └────┬────┘
                │            │
                ▼            ▼
         ┌──────────┐  ┌──────────┐
         │ TOOL REG │  │ RUNTIME  │
         │ 92 TOOLS │  │ CALL     │
         │ 11 CATS  │  │ RETURN   │
         └────┬─────┘  │ EXPRESS  │
              │        │ TRACE    │
              └───┬────┴ STATS    │
                  │    └──────────┘
                  ▼
         ┌──────────────┐
         │  EXECUTION   │
         │ resolution   │
         │ binding      │
         │ execution    │
         │ evaluation   │
         │ error handle │
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ OBSERVABILITY│
         │ result       │
         │ return_value │
         │ last_result  │
         │ output       │
         │ trace        │
         │ stats        │
         └──────────────┘
```

## File System

```text
GET  /files
POST /files/upload
GET  /files/{filename}
PUT  /files/{filename}
DEL  /files/{filename}
POST /files/run/{filename}
```

## Quick Routes

```text
/math/{operation}
/string/{operation}
/date/{operation}
/random/{operation}
/crypto/{operation}
```

## SSE3

```text
/script/stream — STANDBY
```