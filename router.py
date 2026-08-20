#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ROKO ROUTER — router.py
================================================================================
Camada de orquestração: junta o motor da linguagem (roko.py) com o
registro de ferramentas (tools.py) e expõe uma interface limpa e estável
para a camada HTTP (api.py) consumir — sem que api.py precise conhecer
detalhes internos do interpretador ou da lista de ferramentas.

Também concentra: configuração da aplicação (nome, versão, limites de
segurança), gestão dos diretórios de dados (uploads/exemplos/logs) e os
helpers de arquivo `.roko` usados pelos endpoints /files/*.

Por que um arquivo à parte, entre tools.py/roko.py e api.py? Separar
"o que a aplicação faz" (aqui) de "como isso é exposto por HTTP" (api.py)
significa que dá para trocar o framework web (Flask -> Quart -> outro)
sem tocar em lógica de negócio, e dá para testar run_script()/
validate_script() direto, sem precisar subir um servidor.
================================================================================
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from werkzeug.utils import secure_filename

from roko import RokoBlockParser, RokoInterpreter, ExpressionError
from tools import (
    TOOL_SPECS,
    TOOL_VERSION,
    execute_tool,
    meta_categories,
    meta_help,
    meta_info,
    meta_search,
    meta_tools,
)

# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================================
APP_NAME = "ROKO ROUTER"
APP_VERSION = "2.1.0"
API_VERSION = "v1"

# Limites de segurança da API (uso em api.py)
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MiB
REQUEST_TIMEOUT = 30  # segundos

# ============================================================================
# CAMINHOS DO SISTEMA
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
EXAMPLES_FOLDER = BASE_DIR / "examples"
LOGS_FOLDER = BASE_DIR / "logs"
TEMP_FOLDER = BASE_DIR / "temp"

for _folder in (UPLOAD_FOLDER, EXAMPLES_FOLDER, LOGS_FOLDER, TEMP_FOLDER):
    _folder.mkdir(parents=True, exist_ok=True)


# ============================================================================
# EXECUÇÃO E VALIDAÇÃO DE SCRIPTS (fachada sobre roko.py)
# ============================================================================

def run_script(
    script: str,
    variables: Optional[Dict[str, Any]] = None,
    debug: bool = False,
    on_event: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """
    Executa um script ROKO Script. Fachada fina sobre RokoInterpreter —
    existe para que api.py (e qualquer outro consumidor) não precise
    instanciar o interpretador diretamente nem conhecer roko.py.

    Args:
        script: código-fonte ROKO Script
        variables: variáveis iniciais
        debug: ativa impressão de stack trace em erros inesperados
        on_event: callback opcional para streaming em tempo real (ver
            roko.RokoInterpreter.execute) — usado por /script/stream

    Returns:
        O mesmo dict retornado por RokoInterpreter.execute(): success,
        output, trace, variables, return_value, last_result, stats
        (e "error" quando success=False).
    """
    interpreter = RokoInterpreter()
    return interpreter.execute(script, variables=variables, debug=debug, on_event=on_event)


def validate_script(script: str) -> Dict[str, Any]:
    """
    Valida a SINTAXE de um script sem executar nada (nenhuma tool é
    chamada). Fachada sobre RokoBlockParser.

    Returns:
        {"valid": bool, "errors": [str, ...], "line_count": int}
    """
    errors: List[str] = []
    try:
        RokoBlockParser().parse(script)
    except ExpressionError as e:
        errors.append(str(e))
    except Exception as e:
        errors.append(f"Erro inesperado ao validar: {e}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "line_count": len(script.splitlines()),
    }


# ============================================================================
# FERRAMENTAS (fachada sobre tools.py)
# ============================================================================

def call_tool(tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa uma ferramenta isolada (fora de um script). Fachada sobre execute_tool()."""
    return execute_tool(tool_name, params)


def list_tools() -> Dict[str, Dict[str, Any]]:
    """Todas as ferramentas disponíveis (nativas + meta.*)."""
    return meta_tools()


def list_categories() -> Dict[str, List[str]]:
    """Categorias disponíveis e as ferramentas de cada uma."""
    return meta_categories()


def tools_by_category(category: str) -> List[str]:
    """Nomes das ferramentas de uma categoria específica."""
    return meta_categories().get(category, [])


def search_tools(query: str) -> List[Dict[str, Any]]:
    """Busca ferramentas por termo (nome, descrição ou parâmetro)."""
    return meta_search(query)


def tool_help(tool_name: str) -> Dict[str, Any]:
    """Detalhe de uma ferramenta específica."""
    return meta_help(tool_name)


def app_info() -> Dict[str, Any]:
    """Informações gerais da aplicação (nome, versões, contagem de ferramentas)."""
    return meta_info()


# ============================================================================
# ARQUIVOS .roko (uploads e exemplos)
# ============================================================================

def safe_roko_filename(filename: str) -> str:
    """
    Sanitiza um nome de arquivo ROKO.

    Raises:
        ValueError: se o nome for inválido.
    """
    clean = secure_filename(filename)
    if not clean:
        raise ValueError("Nome de arquivo inválido")

    if not clean.lower().endswith(".roko"):
        clean += ".roko"

    return clean


def find_roko_file(filename: str) -> Tuple[Optional[Path], Optional[str]]:
    """
    Localiza um arquivo .roko em uploads/ ou examples/.

    Returns:
        (caminho, origem) onde origem é "user" ou "examples", ou
        (None, None) se não encontrado / nome inválido.
    """
    try:
        clean = safe_roko_filename(filename)
    except ValueError:
        return None, None

    upload_path = UPLOAD_FOLDER / clean
    if upload_path.exists() and upload_path.is_file():
        return upload_path, "user"

    example_path = EXAMPLES_FOLDER / clean
    if example_path.exists() and example_path.is_file():
        return example_path, "examples"

    return None, None
