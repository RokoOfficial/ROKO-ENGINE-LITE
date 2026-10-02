"""
Registro central de ferramentas do ROKO ENGINE LITE.

Use: from TOOLS import execute_tool, TOOL_SPECS, meta_search, ...
"""
# Import lazy-safe: registry carrega tools por path, sem cascade de pacote
from .registry import (  # noqa: F401
    TOOL_SPECS,
    TOOL_VERSION,
    APP_NAME,
    APP_VERSION,
    API_VERSION,
    REQUEST_TIMEOUT,
    RokoTools,
    execute_tool,
    meta_categories,
    meta_tools,
    meta_help,
    meta_info,
    meta_search,
)

__all__ = [
    "TOOL_SPECS",
    "TOOL_VERSION",
    "APP_NAME",
    "APP_VERSION",
    "API_VERSION",
    "REQUEST_TIMEOUT",
    "RokoTools",
    "execute_tool",
    "meta_categories",
    "meta_tools",
    "meta_help",
    "meta_info",
    "meta_search",
]
