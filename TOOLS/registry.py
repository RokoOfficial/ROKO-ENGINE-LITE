#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Registro central de ferramentas do ROKO ENGINE LITE.

Fontes:
  1) TOOLS/<cat>/<tool>/{tool.py,spec.py}  → tools nativas Python
     também registadas como native.<nome>  (para .roko chamarem sem recursão)
  2) Oracle/<cat>/<tool>.roko              → tools em idioma ROKO (prioridade)

CALL nome → se existir .roko no Oracle, executa o script; senão Python.
Dentro de um .roko, CALL native.x.y usa sempre a implementação Python.
"""
from __future__ import annotations

import importlib.util
import inspect
import sys
import threading
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

TOOL_VERSION = "1.1.0"
REQUEST_TIMEOUT = 30
APP_NAME = "ROKO ROUTER"
APP_VERSION = "2.3.1"
API_VERSION = "v1"

_ROOT = Path(__file__).resolve().parent
_PROJECT = _ROOT.parent
_ORACLE = _PROJECT / "Oracle"
LOGS_FOLDER = _PROJECT / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

# stack de tools .roko em execução (anti-recursão)
_roko_stack: List[str] = []
_stack_lock = threading.Lock()


def _load_module(mod_name: str, file_path: Path):
    if mod_name in sys.modules:
        return sys.modules[mod_name]
    spec = importlib.util.spec_from_file_location(mod_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível carregar {file_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _discover_python_tools() -> Dict[str, Dict[str, Any]]:
    specs: Dict[str, Dict[str, Any]] = {}
    for cat_dir in sorted(_ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith(("_", ".")):
            continue
        if cat_dir.name == "__pycache__":
            continue
        for tool_dir in sorted(cat_dir.iterdir()):
            if not tool_dir.is_dir() or tool_dir.name.startswith(("_", ".")):
                continue
            if tool_dir.name == "__pycache__":
                continue
            tool_py = tool_dir / "tool.py"
            spec_py = tool_dir / "spec.py"
            if not tool_py.exists() or not spec_py.exists():
                continue
            tool_mod_name = f"_roko_tool_{cat_dir.name}_{tool_dir.name}"
            try:
                tool_mod = _load_module(tool_mod_name, tool_py)
            except Exception as e:
                print(f"[TOOLS] erro tool.py {tool_dir}: {e}")
                continue
            spec_src = spec_py.read_text(encoding="utf-8")
            ns: Dict[str, Any] = {"__name__": f"_roko_spec_{cat_dir.name}_{tool_dir.name}"}
            callables = {
                n: getattr(tool_mod, n)
                for n in dir(tool_mod)
                if callable(getattr(tool_mod, n, None)) and not n.startswith("_")
            }
            ns.update(callables)
            lines = []
            for line in spec_src.splitlines():
                if line.strip().startswith("from .tool import"):
                    continue
                if line.strip().startswith("from __future__"):
                    continue
                lines.append(line)
            try:
                exec(compile("\n".join(lines), str(spec_py), "exec"), ns)
            except Exception as e:
                print(f"[TOOLS] erro spec.py {tool_dir}: {e}")
                continue
            name = ns.get("NAME")
            fn = ns.get("FN")
            if not name or not callable(fn):
                continue
            entry = {
                "kind": "python",
                "fn": fn,
                "category": ns.get("CATEGORY", cat_dir.name),
                "description": ns.get("DESCRIPTION", ""),
                "parameters": list(ns.get("PARAMETERS") or []),
                "path": None,
            }
            specs[name] = entry
            # alias nativo para tools .roko poderem chamar sem recursão
            specs[f"native.{name}"] = dict(entry)
            specs[f"native.{name}"]["description"] = f"(native) {entry['description']}"
    return specs


def _discover_all() -> Dict[str, Dict[str, Any]]:
    specs = _discover_python_tools()
    try:
        from engine.roko_tool import discover_oracle_roko

        oracle_specs = discover_oracle_roko(_ORACLE)
        # Oracle .roko tem prioridade no nome público (não sobrescreve native.*)
        for name, entry in oracle_specs.items():
            if name.startswith("native."):
                continue
            specs[name] = entry
    except Exception as e:
        print(f"[TOOLS] Oracle .roko discovery: {e}")
    return specs


TOOL_SPECS: Dict[str, Dict[str, Any]] = _discover_all()


class RokoTools:
    """Namespace legado — implementações em TOOLS/<cat>/<tool>/tool.py."""
    pass


def meta_categories() -> Dict[str, List[str]]:
    categories: Dict[str, List[str]] = {}
    for name, spec in TOOL_SPECS.items():
        if name.startswith("native."):
            continue
        categories.setdefault(spec["category"], []).append(name)
    categories["meta"] = [
        "meta.tools", "meta.categories", "meta.help", "meta.info", "meta.search"
    ]
    for cat in categories:
        categories[cat] = sorted(set(categories[cat]))
    return dict(sorted(categories.items()))


def meta_tools() -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for name, spec in TOOL_SPECS.items():
        if name.startswith("native."):
            continue
        result[name] = {
            "category": spec["category"],
            "description": spec["description"],
            "parameters": spec.get("parameters", []),
            "kind": spec.get("kind", "python"),
        }
    for m, params in (
        ("meta.tools", []),
        ("meta.categories", []),
        ("meta.help", ["tool_name"]),
        ("meta.info", []),
        ("meta.search", ["query"]),
    ):
        result[m] = {"category": "meta", "description": f"Meta-tool {m}", "parameters": params, "kind": "meta"}
    return result


def meta_help(tool_name: str) -> Dict[str, Any]:
    if tool_name in TOOL_SPECS and not tool_name.startswith("native."):
        spec = TOOL_SPECS[tool_name]
        return {
            "name": tool_name,
            "category": spec["category"],
            "description": spec["description"],
            "parameters": spec.get("parameters", []),
            "kind": spec.get("kind", "python"),
            "path": spec.get("path"),
        }
    if tool_name.startswith("meta."):
        return meta_tools().get(tool_name, {"error": "not found"})
    return {"error": f"Ferramenta '{tool_name}' não encontrada"}


def meta_info() -> Dict[str, Any]:
    public = [n for n in TOOL_SPECS if not n.startswith("native.")]
    roko_n = sum(1 for n in public if TOOL_SPECS[n].get("kind") == "roko")
    py_n = sum(1 for n in public if TOOL_SPECS[n].get("kind") == "python")
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "api_version": API_VERSION,
        "tool_version": TOOL_VERSION,
        "total_tools": len(public) + 5,
        "python_tools": py_n,
        "roko_tools": roko_n,
        "categories": sorted({TOOL_SPECS[n]["category"] for n in public} | {"meta"}),
    }


def _fold_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def meta_search(query: str) -> List[Dict[str, Any]]:
    query = _fold_accents(query.lower().strip())
    results = []
    for name, spec in TOOL_SPECS.items():
        if name.startswith("native."):
            continue
        if (
            query in _fold_accents(name.lower())
            or query in _fold_accents(spec["category"].lower())
            or query in _fold_accents(spec["description"].lower())
            or any(query in _fold_accents(p.lower()) for p in spec.get("parameters", []))
        ):
            results.append({
                "name": name,
                "category": spec["category"],
                "description": spec["description"],
                "parameters": spec.get("parameters", []),
                "kind": spec.get("kind", "python"),
            })
    return sorted(results, key=lambda x: x["name"])


def _accepts_var_positional(fn: Callable) -> bool:
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return False
    return any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values())


def _execute_python(spec: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    fn = spec.get("fn")
    if not callable(fn):
        return {"success": False, "error": "implementação Python em falta"}
    try:
        if _accepts_var_positional(fn):
            values = list(params.values())
            if len(values) == 1 and isinstance(values[0], (list, tuple)):
                args = list(values[0])
            else:
                args = values
            result = fn(*args)
        else:
            result = fn(**params)
        return {"success": True, "result": result}
    except TypeError as e:
        return {"success": False, "error": f"Erro de parâmetros: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _execute_roko(spec: Dict[str, Any], params: Dict[str, Any], tool_name: str) -> Dict[str, Any]:
    from engine.roko_tool import execute_roko_file

    path = Path(spec["path"])
    with _stack_lock:
        if tool_name in _roko_stack:
            # recursão → fallback native
            native = TOOL_SPECS.get(f"native.{tool_name}")
            if native and native.get("kind") == "python":
                return _execute_python(native, params)
            return {"success": False, "error": f"Recursão na tool .roko '{tool_name}'"}
        _roko_stack.append(tool_name)
    try:
        return execute_roko_file(path, params=params)
    finally:
        with _stack_lock:
            if _roko_stack and _roko_stack[-1] == tool_name:
                _roko_stack.pop()


def execute_tool(tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = params or {}
    if tool_name == "meta.tools":
        return {"success": True, "result": meta_tools()}
    if tool_name == "meta.categories":
        return {"success": True, "result": meta_categories()}
    if tool_name == "meta.help":
        return {"success": True, "result": meta_help(params.get("tool_name", ""))}
    if tool_name == "meta.info":
        return {"success": True, "result": meta_info()}
    if tool_name == "meta.search":
        return {"success": True, "result": meta_search(params.get("query", ""))}

    spec = TOOL_SPECS.get(tool_name)
    if spec is None:
        return {"success": False, "error": f"Ferramenta '{tool_name}' não encontrada"}

    kind = spec.get("kind", "python")
    if kind == "roko":
        return _execute_roko(spec, params, tool_name)
    return _execute_python(spec, params)


def reload_tools() -> int:
    """Re-descobre tools Python + Oracle .roko (útil após editar Oracle/)."""
    global TOOL_SPECS
    # limpar módulos tool em cache
    for k in list(sys.modules):
        if k.startswith("_roko_tool_") or k.startswith("_roko_spec_"):
            del sys.modules[k]
    TOOL_SPECS = _discover_all()
    return len([n for n in TOOL_SPECS if not n.startswith("native.")])
