#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor de tools definidas em scripts ROKO (.roko) no Oracle/.

Params da CALL são injectados como variáveis do interpretador.
O valor de RETURN do script é o resultado da tool.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_META_RE = re.compile(
    r"^//\s*@(\w+)\s*:\s*(.+)$",
    re.MULTILINE,
)


def parse_roko_meta(source: str, fallback_name: str, fallback_cat: str) -> Dict[str, Any]:
    """Extrai metadados // @key: value do cabeçalho do .roko."""
    meta: Dict[str, Any] = {
        "name": fallback_name,
        "category": fallback_cat,
        "description": "",
        "parameters": [],
    }
    for m in _META_RE.finditer(source):
        key = m.group(1).strip().lower()
        val = m.group(2).strip()
        if key in ("name", "nome"):
            meta["name"] = val
        elif key in ("category", "categoria"):
            meta["category"] = val
        elif key in ("description", "descricao", "desc"):
            meta["description"] = val
        elif key in ("params", "parameters", "parametros"):
            meta["parameters"] = [p.strip() for p in val.split(",") if p.strip()]
    return meta


def execute_roko_file(
    path: Path,
    params: Optional[Dict[str, Any]] = None,
    extra_vars: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Executa um ficheiro .roko como tool.

    Returns:
        {"success": True, "result": ...} ou {"success": False, "error": ...}
    """
    from engine.interpreter import RokoInterpreter

    params = dict(params or {})
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"success": False, "error": f"Não foi possível ler {path}: {e}"}

    variables: Dict[str, Any] = {}
    variables.update(params)
    if extra_vars:
        variables.update(extra_vars)

    interp = RokoInterpreter()
    out = interp.execute(source, variables=variables)
    if not out.get("success"):
        return {
            "success": False,
            "error": out.get("error") or out.get("message") or "erro no script .roko",
            "output": out.get("output"),
        }

    result = out.get("return_value")
    if result is None and out.get("output"):
        # último output legível se não houve RETURN
        result = out["output"][-1] if out["output"] else None

    return {"success": True, "result": result, "trace": out.get("trace"), "output": out.get("output")}


def discover_oracle_roko(oracle_root: Path) -> Dict[str, Dict[str, Any]]:
    """
    Descobre Oracle/<categoria>/<nome>.roko → tool cat.nome

    Ignora: demos/, _*, semantic_router, ficheiros soltos na raiz opcionalmente
    incluídos se forem *.roko com meta.
    """
    specs: Dict[str, Dict[str, Any]] = {}
    if not oracle_root.is_dir():
        return specs

    skip_dirs = {"demos", "demo", "__pycache__", ".git"}

    for cat_dir in sorted(oracle_root.iterdir()):
        if not cat_dir.is_dir():
            continue
        if cat_dir.name.startswith(("_", ".")) or cat_dir.name in skip_dirs:
            continue
        for f in sorted(cat_dir.glob("*.roko")):
            if f.name.startswith("_"):
                continue
            tool_name = f"{cat_dir.name}.{f.stem}"
            try:
                source = f.read_text(encoding="utf-8")
            except Exception as e:
                print(f"[ORACLE] erro a ler {f}: {e}")
                continue
            meta = parse_roko_meta(source, tool_name, cat_dir.name)
            name = meta["name"] or tool_name
            specs[name] = {
                "kind": "roko",
                "path": str(f.resolve()),
                "category": meta["category"] or cat_dir.name,
                "description": meta["description"] or f"Oracle tool {name}",
                "parameters": meta["parameters"],
                "fn": None,
            }
    return specs
