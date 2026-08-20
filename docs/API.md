# API Reference — ROKO ROUTER 2.1.0

## Endpoints

### API Info

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Info da API |
| GET | `/health` | Health check |
| GET | `/version` | Versão |

### Tool System

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/tools` | Lista tools |
| GET | `/categories` | Lista categorias |
| GET | `/search` | Busca tools |
| GET | `/help` | Ajuda |
| GET | `/category` | Tools por categoria |
| POST | `/tool/{name}` | Executa tool |

### Script Engine

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/script/execute` | Executa script |
| POST | `/script/validate` | Valida script |
| POST | `/script/stream` | Stream (SSE3) |

### File System

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/files` | Lista arquivos |
| POST | `/files/upload` | Upload |
| GET | `/files/{filename}` | Lê arquivo |
| PUT | `/files/{filename}` | Atualiza |
| DELETE | `/files/{filename}` | Deleta |
| POST | `/files/run/{filename}` | Executa .roko |

### Quick Routes

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/math/{operation}` | Operação math |
| POST | `/string/{operation}` | Operação string |
| POST | `/date/{operation}` | Operação date |
| POST | `/random/{operation}` | Operação random |
| POST | `/crypto/{operation}` | Operação crypto |

## Categorias (11)

crypto, date, http, json, list, log, math, meta, random, string, system