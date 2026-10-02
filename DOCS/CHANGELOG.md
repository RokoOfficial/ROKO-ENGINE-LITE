# Changelog

## [2.3.1] - 2026-09-12

### Fixed
- `http.get_json`: uso directo de `requests` (removido `RokoTools` indefinido)
- `system.version`: resolução correcta de `APP_VERSION` / `TOOL_VERSION`
- `MAX_EXEC_SECONDS` elevado para 60s (scripts mais longos e testes)

### Changed
- Versão de runtime alinhada em registry e docs (2.3.1)
- Smoke test e nova bateria pesada (`tests/test_battery.py`) — 41 checks
- Documentação (README, ARCHITECTURE) actualizada com diagramas Mermaid e contagens actuais

### Validated
- Registry: 121 Oracle + 5 meta = 126 tools
- Agent.run + HGR store/get/search
- Script engine: SET, CALL, IF, WHILE, RETURN
- HTTP status / get_json (com rede)

## [2.3.1] - 2026-09-11

### Added
- Oracle tools executáveis em `.roko` (`Oracle/<cat>/<name>.roko`)
- Registry: prioridade Oracle; alias `native.*` para Python
- Cobertura: espelho `.roko` de todas as tools dos módulos `TOOLS/`
- Agent simbólico `engine/agent` + tool `agent.run` (sem LLM)
- HGR v5: status, parallel_group, record_steps_batch, MemoryEnhancedAgent
- Plans de exemplo em `plans/`

### Changed
- Demos legados `.hmp` movidos para `Oracle/demos/`
- Documentação alinhada (README, Oracle, ARCHITECTURE, TOOLS)

## [2.3.1] - 2026-09-10

### Added
- HGR + Auth + Cron + Motor Parallel
- Extensão agentic simbólica inicial

## [2.1.0] - 2026-08-20

### Added
- Runtime modular, ROKO Script, SSE, file API, quick routes
