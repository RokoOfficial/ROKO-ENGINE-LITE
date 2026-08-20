#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ROKO ROUTER — api.py
================================================================================
Camada HTTP: expõe router.py (que por sua vez junta roko.py + tools.py)
como uma API REST, em Quart (assíncrono) em vez de Flask — mesmo padrão
usado pela Motor Parallel API e pela ENGINE V14 KNOWLEAGER que também
fazem parte deste projeto: Quart + CORS + streaming via SSE.

Novidade desta versão: POST /script/stream — executa um script ROKO
Script e transmite CADA EVENTO de execução (SET, CALL, IF, laços,
RETURN...) via Server-Sent Events, no INSTANTE em que acontece — não é
uma simulação: o script roda numa thread separada (o interpretador é
síncrono) e cada evento é publicado numa fila assíncrona assim que o
interpretador o gera (via o hook `on_event` de roko.RokoInterpreter),
para o generator SSE consumir e enviar ao cliente em tempo real.
================================================================================
"""
from __future__ import annotations

import asyncio
import datetime as dt
import json
import sys
from typing import Any, Dict

from quart import Quart, request, jsonify, Response
from quart_cors import cors

import router
from tools import TOOL_SPECS, TOOL_VERSION, execute_tool, meta_categories, meta_help, meta_search, meta_tools

# ============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO QUART
# ============================================================================

app = Quart(__name__)
app.config["MAX_CONTENT_LENGTH"] = router.MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = __import__("os").environ.get("ROKO_SECRET_KEY", "roko-router-default-key-change-me")

# CORS liberado para todas as origens (mesmo padrão dos outros serviços do
# projeto — ajuste allow_origin para uma lista fechada em produção).
app = cors(app, allow_origin="*", allow_headers=["Content-Type", "Authorization"], allow_methods=["GET", "POST", "PUT", "DELETE"])


def _err(message: str, status: int = 400, **extra: Any) -> tuple:
    payload = {"success": False, "error": message}
    payload.update(extra)
    return jsonify(payload), status


# ============================================================================
# ENDPOINTS - INFORMAÇÕES GERAIS
# ============================================================================

@app.route("/", methods=["GET"])
async def home():
    """Endpoint raiz — informações da API e mapa de endpoints."""
    return jsonify({
        "name": router.APP_NAME,
        "version": router.APP_VERSION,
        "api_version": router.API_VERSION,
        "description": "API de automação e execução de ferramentas (Quart, CORS, SSE)",
        "status": "online",
        "total_tools": len(TOOL_SPECS) + 5,
        "categories": len(meta_categories()),
        "endpoints": {
            "info": {"root": "GET /", "health": "GET /health", "version": "GET /version"},
            "tools": {
                "list": "GET /tools", "categories": "GET /tools/categories",
                "by_category": "GET /tools/category/{category}", "execute": "POST /tool/{tool_name}",
                "search": "GET /tools/search?q={query}", "help": "GET /tools/help/{tool_name}",
            },
            "scripts": {
                "execute": "POST /script/execute",
                "stream": "POST /script/stream  (SSE — eventos em tempo real)",
                "validate": "POST /script/validate",
            },
            "files": {
                "list": "GET /files", "upload": "POST /files/upload", "get": "GET /files/{filename}",
                "update": "PUT /files/{filename}", "delete": "DELETE /files/{filename}",
                "run": "POST /files/run/{filename}",
            },
            "quick": {
                "math": "/math/{operation}", "string": "/string/{operation}",
                "date": "/date/{operation}", "random": "/random/{operation}", "crypto": "/crypto/{operation}",
            },
        },
    })


@app.route("/health", methods=["GET"])
async def health_check():
    """Health check simples."""
    return jsonify({"status": "healthy", "timestamp": dt.datetime.now().isoformat(), "version": router.APP_VERSION})


@app.route("/version", methods=["GET"])
async def get_version():
    """Informações de versão."""
    return jsonify({
        "name": router.APP_NAME, "version": router.APP_VERSION, "api_version": router.API_VERSION,
        "tool_version": TOOL_VERSION, "python_version": sys.version, "platform": sys.platform,
    })


# ============================================================================
# ENDPOINTS - FERRAMENTAS (TOOLS)
# ============================================================================

@app.route("/tools", methods=["GET"])
async def list_tools_route():
    """Lista ferramentas, com filtro opcional por categoria e/ou busca por termo."""
    category = request.args.get("category")
    search = request.args.get("search")

    tools = meta_tools()
    if category:
        tools = {name: spec for name, spec in tools.items() if spec.get("category") == category}
    if search:
        search_lower = search.lower()
        tools = {
            name: spec for name, spec in tools.items()
            if (search_lower in name.lower() or search_lower in spec.get("description", "").lower()
                or any(search_lower in p.lower() for p in spec.get("parameters", [])))
        }

    return jsonify({"total": len(tools), "tools": tools})


@app.route("/tools/categories", methods=["GET"])
async def list_categories_route():
    """Lista todas as categorias de ferramentas."""
    return jsonify({"total": len(meta_categories()), "categories": meta_categories()})


@app.route("/tools/category/<category>", methods=["GET"])
async def get_tools_by_category_route(category: str):
    """Lista ferramentas de uma categoria específica."""
    categories = meta_categories()
    if category not in categories:
        return await _err(f"Categoria '{category}' não encontrada", 404)

    tool_names = categories[category]
    all_tools = meta_tools()
    tools = {name: all_tools[name] for name in tool_names if name in all_tools}
    return jsonify({"category": category, "count": len(tools), "tools": tools})


@app.route("/tools/search", methods=["GET"])
async def search_tools_route():
    """Busca ferramentas por termo (query param `q`)."""
    query = request.args.get("q", "")
    if not query:
        return await _err("Parâmetro 'q' é obrigatório", 400)

    results = meta_search(query)
    return jsonify({"query": query, "count": len(results), "results": results})


@app.route("/tools/help/<tool_name>", methods=["GET"])
async def get_tool_help_route(tool_name: str):
    """Ajuda detalhada sobre uma ferramenta."""
    return jsonify(meta_help(tool_name))


@app.route("/tool/<tool_name>", methods=["POST"])
async def execute_tool_endpoint(tool_name: str):
    """Executa uma ferramenta isolada com os parâmetros do corpo JSON."""
    try:
        data = await request.get_json(silent=True) or {}
    except Exception:
        return await _err("JSON inválido", 400)

    result = execute_tool(tool_name, data)
    status = 200 if result["success"] else 400
    return jsonify({"tool": tool_name, **result}), status


# ============================================================================
# ENDPOINTS - SCRIPTS
# ============================================================================

@app.route("/script/execute", methods=["POST"])
async def execute_script():
    """
    Executa um script ROKO Script síncrono/completo (sem streaming — para
    isso, use POST /script/stream).

    Request Body:
        {"script": "...", "variables": {...opcional}, "debug": bool opcional}
    """
    data = await request.get_json(silent=True) or {}
    script = data.get("script", "")
    variables = data.get("variables", {})
    debug = data.get("debug", False)

    if not isinstance(script, str) or not script.strip():
        return await _err("Script não fornecido", 400)
    if not isinstance(variables, dict):
        return await _err("variables deve ser um objeto", 400)

    result = router.run_script(script, variables, debug)
    status = 200 if result["success"] else 400
    return jsonify(result), status


@app.route("/script/stream", methods=["POST"])
async def stream_script():
    """
    Executa um script ROKO Script e transmite cada evento de execução via
    Server-Sent Events, EM TEMPO REAL (não é o trace completo mandado de
    uma vez no final — cada evento chega assim que o interpretador o gera).

    Request Body: igual a /script/execute.

    Eventos SSE emitidos:
        event: start     — {"script_lines": N}
        event: trace      — um evento de execução (mesmo formato de cada
                             item de "trace" em /script/execute: set, call,
                             if, while_start/end, for_start/end, return,
                             break, continue, expr, error)
        event: done        — resultado final completo (mesmo payload de
                              /script/execute: success, output, trace,
                              variables, return_value, stats)
    """
    data = await request.get_json(silent=True) or {}
    script = data.get("script", "")
    variables = data.get("variables", {})
    debug = data.get("debug", False)

    if not isinstance(script, str) or not script.strip():
        return await _err("Script não fornecido", 400)
    if not isinstance(variables, dict):
        return await _err("variables deve ser um objeto", 400)

    async def event_stream():
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue = asyncio.Queue()
        SENTINEL = object()

        def on_event(ev: Dict[str, Any]) -> None:
            # Chamado de dentro da thread do interpretador — nunca toque
            # diretamente numa asyncio.Queue de outra thread; agenda a
            # inserção de volta no loop principal.
            loop.call_soon_threadsafe(queue.put_nowait, ev)

        def run_blocking() -> Dict[str, Any]:
            result = router.run_script(script, variables, debug, on_event=on_event)
            loop.call_soon_threadsafe(queue.put_nowait, SENTINEL)
            return result

        yield f"event: start\ndata: {json.dumps({'script_lines': len(script.splitlines())})}\n\n"

        task = asyncio.ensure_future(asyncio.to_thread(run_blocking))

        while True:
            item = await queue.get()
            if item is SENTINEL:
                break
            yield f"event: trace\ndata: {json.dumps(item, ensure_ascii=False, default=str)}\n\n"

        result = await task
        yield f"event: done\ndata: {json.dumps(result, ensure_ascii=False, default=str)}\n\n"

    return Response(event_stream(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })


@app.route("/script/validate", methods=["POST"])
async def validate_script():
    """
    Valida a SINTAXE de um script sem executá-lo (sem efeitos colaterais —
    nenhuma ferramenta é chamada, nenhum CALL roda).
    """
    data = await request.get_json(silent=True) or {}
    script = data.get("script", "")

    if not isinstance(script, str) or not script.strip():
        return await _err("Script não fornecido", 400)

    return jsonify(router.validate_script(script))


# ============================================================================
# ENDPOINTS - ARQUIVOS
# ============================================================================

@app.route("/files", methods=["GET"])
async def list_files():
    """Lista todos os arquivos .roko disponíveis (uploads + exemplos)."""
    files = []
    for folder, source in [(router.UPLOAD_FOLDER, "user"), (router.EXAMPLES_FOLDER, "examples")]:
        for path in sorted(folder.glob("*.roko")):
            try:
                stat = path.stat()
                files.append({
                    "name": path.name, "size": stat.st_size, "source": source,
                    "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "created": dt.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                })
            except OSError:
                continue
    return jsonify({"count": len(files), "files": files})


@app.route("/files/upload", methods=["POST"])
async def upload_file():
    """Cria um novo arquivo .roko em uploads/."""
    data = await request.get_json(silent=True) or {}
    filename = data.get("filename", "").strip()
    content = data.get("content", "")

    if not filename:
        return await _err("Nome do arquivo é obrigatório", 400)
    if not isinstance(content, str):
        return await _err("content deve ser uma string", 400)

    try:
        filename = router.safe_roko_filename(filename)
    except ValueError as e:
        return await _err(str(e), 400)

    example_path = router.EXAMPLES_FOLDER / filename
    if example_path.exists():
        return await _err(f"Arquivo '{filename}' existe na pasta de exemplos e não pode ser sobrescrito", 409)

    path = router.UPLOAD_FOLDER / filename
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as e:
        return await _err(f"Erro ao salvar: {e}", 500)

    return jsonify({
        "success": True, "message": f"Arquivo '{filename}' criado com sucesso",
        "filename": filename, "size": len(content.encode("utf-8")), "source": "user",
    })


@app.route("/files/<filename>", methods=["GET"])
async def get_file(filename: str):
    """Obtém o conteúdo de um arquivo .roko."""
    path, source = router.find_roko_file(filename)
    if path is None:
        return await _err(f"Arquivo '{filename}' não encontrado", 404)

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        return await _err(f"Erro ao ler arquivo: {e}", 500)

    stat = path.stat()
    return jsonify({
        "filename": path.name, "content": content, "source": source,
        "size": stat.st_size, "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(),
    })


@app.route("/files/<filename>", methods=["PUT"])
async def update_file(filename: str):
    """Atualiza o conteúdo de um arquivo .roko existente (em uploads/)."""
    try:
        clean = router.safe_roko_filename(filename)
    except ValueError as e:
        return await _err(str(e), 400)

    path = router.UPLOAD_FOLDER / clean
    if not path.exists():
        return await _err(f"Arquivo '{filename}' não encontrado", 404)

    data = await request.get_json(silent=True) or {}
    content = data.get("content", "")
    if not isinstance(content, str):
        return await _err("content deve ser uma string", 400)

    try:
        path.write_text(content, encoding="utf-8")
    except OSError as e:
        return await _err(f"Erro ao salvar: {e}", 500)

    return jsonify({
        "success": True, "message": f"Arquivo '{clean}' atualizado com sucesso",
        "filename": clean, "size": len(content.encode("utf-8")),
    })


@app.route("/files/<filename>", methods=["DELETE"])
async def delete_file(filename: str):
    """Remove um arquivo .roko de uploads/."""
    try:
        clean = router.safe_roko_filename(filename)
    except ValueError as e:
        return await _err(str(e), 400)

    path = router.UPLOAD_FOLDER / clean
    if not path.exists():
        return await _err(f"Arquivo '{filename}' não encontrado", 404)

    try:
        path.unlink()
    except OSError as e:
        return await _err(f"Erro ao remover: {e}", 500)

    return jsonify({"success": True, "message": f"Arquivo '{clean}' removido com sucesso"})


@app.route("/files/run/<filename>", methods=["POST"])
async def run_file(filename: str):
    """Executa um arquivo .roko existente (uploads/ ou examples/)."""
    path, source = router.find_roko_file(filename)
    if path is None:
        return await _err(f"Arquivo '{filename}' não encontrado", 404)

    data = await request.get_json(silent=True) or {}
    variables = data.get("variables", {})
    debug = data.get("debug", False)
    if not isinstance(variables, dict):
        return await _err("variables deve ser um objeto", 400)

    try:
        script = path.read_text(encoding="utf-8")
    except OSError as e:
        return await _err(f"Erro ao ler arquivo: {e}", 500)

    result = router.run_script(script, variables, debug)
    result["filename"] = path.name
    result["source"] = source

    status = 200 if result["success"] else 400
    return jsonify(result), status


# ============================================================================
# ENDPOINTS - OPERAÇÕES RÁPIDAS
# ============================================================================

_QUICK_PARAM_KEYS = {
    "math": ["a", "b", "n", "value", "decimals"],
    "string": ["text", "old", "new", "substring", "prefix", "suffix", "length", "char"],
    "date": ["date_str", "format_str", "days", "hours", "date1", "date2"],
    "random": ["min_val", "max_val", "items", "length"],
    "crypto": ["text", "length"],
}

_QUICK_TOOL_MAP = {
    "math": {
        "sum": "math.sum", "add": "math.sum", "subtract": "math.subtract", "sub": "math.subtract",
        "multiply": "math.multiply", "mul": "math.multiply", "divide": "math.divide", "div": "math.divide",
        "power": "math.power", "pow": "math.power", "sqrt": "math.sqrt", "abs": "math.abs",
        "floor": "math.floor", "ceil": "math.ceil", "round": "math.round", "factorial": "math.factorial",
        "percentage": "math.percentage", "average": "math.average",
    },
    "string": {
        "upper": "string.upper", "lower": "string.lower", "capitalize": "string.capitalize",
        "title": "string.title", "reverse": "string.reverse", "length": "string.length",
        "len": "string.length", "trim": "string.trim", "replace": "string.replace", "split": "string.split",
        "join": "string.join", "contains": "string.contains", "starts_with": "string.starts_with",
        "ends_with": "string.ends_with", "find": "string.find", "slice": "string.slice",
        "append": "string.append", "count": "string.count", "pad_left": "string.pad_left",
        "pad_right": "string.pad_right",
    },
    "date": {
        "now": "date.now", "timestamp": "date.timestamp", "format": "date.format",
        "add_days": "date.add_days", "add_hours": "date.add_hours", "diff_days": "date.diff_days",
        "parse": "date.parse",
    },
    "random": {
        "number": "random.number", "int": "random.number", "float": "random.float",
        "choice": "random.choice", "shuffle": "random.shuffle", "boolean": "random.boolean", "bool": "random.boolean",
    },
    "crypto": {
        "uuid": "crypto.uuid", "hash": "crypto.hash", "md5": "crypto.md5", "sha1": "crypto.sha1",
        "random_string": "crypto.random_string",
    },
}


async def _quick_endpoint(group: str, operation: str):
    data = await request.get_json(silent=True) or {}
    params = {}
    for key in _QUICK_PARAM_KEYS[group]:
        value = request.args.get(key, data.get(key))
        if value is not None:
            params[key] = value

    tool_name = _QUICK_TOOL_MAP[group].get(operation)
    if not tool_name:
        return await _err(f"Operação '{operation}' não suportada", 400)

    result = execute_tool(tool_name, params)
    if not result["success"]:
        return jsonify(result), 400

    return jsonify({"operation": operation, "tool": tool_name, "result": result["result"]})


@app.route("/math/<operation>", methods=["GET", "POST"])
async def quick_math(operation: str):
    """Endpoints rápidos para operações matemáticas (ex.: GET /math/sum?a=10&b=5)."""
    return await _quick_endpoint("math", operation)


@app.route("/string/<operation>", methods=["GET", "POST"])
async def quick_string(operation: str):
    """Endpoints rápidos para operações com strings (ex.: GET /string/upper?text=hello)."""
    return await _quick_endpoint("string", operation)


@app.route("/date/<operation>", methods=["GET", "POST"])
async def quick_date(operation: str):
    """Endpoints rápidos para operações com datas (ex.: GET /date/now)."""
    return await _quick_endpoint("date", operation)


@app.route("/random/<operation>", methods=["GET", "POST"])
async def quick_random(operation: str):
    """Endpoints rápidos para operações aleatórias (ex.: GET /random/number?min_val=1&max_val=10)."""
    return await _quick_endpoint("random", operation)


@app.route("/crypto/<operation>", methods=["GET", "POST"])
async def quick_crypto(operation: str):
    """Endpoints rápidos para operações criptográficas (ex.: GET /crypto/uuid)."""
    return await _quick_endpoint("crypto", operation)


# ============================================================================
# TRATAMENTO DE ERROS
# ============================================================================

@app.errorhandler(404)
async def not_found(error):
    return jsonify({"success": False, "error": "Rota não encontrada", "path": request.path, "method": request.method}), 404


@app.errorhandler(413)
async def request_too_large(error):
    return jsonify({"success": False, "error": f"Payload excede o limite de {router.MAX_CONTENT_LENGTH // (1024 * 1024)} MiB"}), 413


@app.errorhandler(405)
async def method_not_allowed(error):
    return jsonify({"success": False, "error": "Método não permitido"}), 405


@app.errorhandler(Exception)
async def handle_exception(error):
    app.logger.error(f"Erro não tratado: {error}")
    if app.debug:
        return jsonify({"success": False, "error": str(error), "type": type(error).__name__}), 500
    return jsonify({"success": False, "error": "Erro interno do servidor"}), 500


# ============================================================================
# MIDDLEWARE DE LOG
# ============================================================================

@app.before_request
async def log_request():
    if request.path.startswith("/files") and request.method in ("PUT", "POST", "DELETE"):
        app.logger.info(f"[{request.method}] {request.path}")
    elif request.path.startswith("/tool") or request.path.startswith("/script"):
        app.logger.info(f"[{request.method}] {request.path}")


@app.after_request
async def log_response(response):
    if response.status_code >= 400:
        app.logger.warning(f"[{response.status_code}] {request.method} {request.path}")
    return response


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8989))
    host = os.environ.get("HOST", "0.0.0.0")
    debug_mode = os.environ.get("ROKO_DEBUG", "false").lower() == "true"

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
       {router.APP_NAME} v{router.APP_VERSION} — API de Automação (Quart)
    ╚══════════════════════════════════════════════════════════════╝

    Servidor:    http://{host}:{port}
    Ferramentas: {len(TOOL_SPECS) + 5}
    Debug:       {debug_mode}

    Módulos:     tools.py (ferramentas) + roko.py (motor) + router.py
                 (orquestração) + api.py (este arquivo — HTTP/Quart/CORS/SSE)
    """)

    app.run(host=host, port=port, debug=debug_mode)
