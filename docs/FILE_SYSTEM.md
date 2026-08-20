# File System — ROKO ROUTER 2.1.0

## Visão Geral

Sistema de arquivos para armazenar e executar scripts `.roko`.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/files` | Lista arquivos |
| POST | `/files/upload` | Upload de arquivo |
| GET | `/files/{filename}` | Lê arquivo |
| PUT | `/files/{filename}` | Atualiza arquivo |
| DELETE | `/files/{filename}` | Deleta arquivo |
| POST | `/files/run/{filename}` | Executa .roko |

## Fluxo

```text
POST /files/upload
        │
        ▼
   arquivo.roko
        │
        ▼
   Storage / Files
        │
        │ POST /files/run/{filename}
        ▼
   Runtime Engine
        │
        ├── parse
        ├── expression
        ├── CALL
        ├── RETURN
        │
        ▼
   Execution Trace
        │
        ├── output
        ├── return_value
        ├── last_result
        ├── stats
        └── variables
        │
        ▼
      Cliente
```

## Exemplo de Upload

```bash
curl -X POST /files/upload \
  -F "file=@script.roko"
```

## Exemplo de Execução

```bash
curl -X POST /files/run/script.roko
```

## Resposta

```json
{
  "output": "...",
  "return_value": "...",
  "last_result": "...",
  "stats": {
    "tool_calls": 2,
    "loop_steps": 0
  }
}
```