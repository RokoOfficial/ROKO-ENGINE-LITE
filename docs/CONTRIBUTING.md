# Contribuindo — ROKO ROUTER 2.1.0

## Como contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas mudanças
4. Envie um Pull Request

## Padrões de código

### Python

- Seguir PEP 8
- Usar type hints
- Documentar funções com docstrings

### Commits

- Usar mensagens claras e descritivas
- Referenciar issues quando aplicável

## Estrutura de diretórios

```text
ROKO-ENGINE-LITE/
├── docs/          # Documentação
├── src/           # Código fonte
│   ├── tools/     # Tools registradas
│   ├── engine/    # Runtime engine
│   └── api/       # Endpoints
├── tests/         # Testes
├── main.py        # Entry point
└── requirements.txt
```

## Testes

```bash
pytest tests/
```

## Pull Requests

- Descreva claramente as mudanças
- Inclua testes quando aplicável
- Atualize a documentação se necessário

## Issues

- Use templates fornecidos
- Descreva o problema claramente
- Inclua passos para reproduzir