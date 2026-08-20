# Instalação — ROKO ROUTER 2.1.0

## Requisitos

- Python 3.10+
- pip

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/RokoOfficial/ROKO-ENGINE-LITE.git
cd ROKO-ENGINE-LITE
```

### 2. Crie um virtualenv (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor

```bash
python main.py
```

### 5. Verifique

```bash
curl http://localhost:8000/health
```

```json
{"status": "ok"}
```

## Dependências

| Pacote | Versão |
|--------|--------|
| quart | 0.19+ |
| quart-cors | 0.7+ |
| sse-starlette | 2.0+ |

## Configuração

### Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `HOST` | `0.0.0.0` | Host do servidor |
| `PORT` | `8000` | Porta do servidor |
| `DEBUG` | `false` | Modo debug |

### Exemplo

```bash
export HOST=0.0.0.0
export PORT=8080
export DEBUG=true
python main.py
```