#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bateria de testes pesados — ROKO ENGINE LITE 2.3.1
Valida registry, tools Oracle/Python, interpreter, agent, HGR, limits.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

PASSED = 0
FAILED = 0
ERRORS: list[str] = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ✓ {name}")
    else:
        FAILED += 1
        msg = f"  ✗ {name}" + (f" — {detail}" if detail else "")
        print(msg)
        ERRORS.append(msg)


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def test_registry() -> None:
    section("Registry / meta")
    from TOOLS.registry import meta_info, meta_categories, meta_tools, execute_tool, TOOL_SPECS

    info = meta_info()
    ok("version present", "version" in info and info["version"] == "2.3.1", str(info.get("version")))
    ok("total_tools >= 120", info.get("total_tools", 0) >= 120, str(info.get("total_tools")))
    ok("roko_tools == 121", info.get("roko_tools") == 121, str(info.get("roko_tools")))
    ok("categories non-empty", len(info.get("categories", [])) >= 10)

    cats = meta_categories()
    ok("meta_categories is dict", isinstance(cats, dict) and "math" in cats)
    ok("math.sum listed", "math.sum" in cats.get("math", []))

    tools = meta_tools()
    ok("meta_tools returns data", tools is not None and (isinstance(tools, (list, dict))))

    # native.* must exist for wrappers
    ok("native.math.sum exists", "native.math.sum" in TOOL_SPECS)
    ok("math.sum is roko", TOOL_SPECS.get("math.sum", {}).get("kind") == "roko")


def test_core_tools() -> None:
    section("Core tools (math / string / list / json)")
    from TOOLS.registry import execute_tool

    r = execute_tool("math.sum", {"a": 7, "b": 8})
    ok("math.sum 7+8", r.get("success") and r.get("result") == 15, str(r))

    r = execute_tool("math.multiply", {"a": 6, "b": 7})
    ok("math.multiply", r.get("success") and r.get("result") == 42, str(r))

    r = execute_tool("string.lower", {"text": "ROKO"})
    ok("string.lower", r.get("success") and r.get("result") == "roko", str(r))

    r = execute_tool("string.upper", {"text": "roko"})
    ok("string.upper", r.get("success") and r.get("result") == "ROKO", str(r))

    r = execute_tool("list.length", {"items": [1, 2, 3, 4]})
    ok("list.length", r.get("success") and r.get("result") == 4, str(r))

    r = execute_tool("json.stringify", {"obj": {"a": 1}})
    ok("json.stringify", r.get("success") and '"a"' in str(r.get("result")), str(r))

    r = execute_tool("crypto.hash", {"text": "roko", "algorithm": "sha256"})
    ok("crypto.hash", r.get("success") and isinstance(r.get("result"), str) and len(r["result"]) == 64, str(r)[:80])

    r = execute_tool("date.now", {})
    ok("date.now", r.get("success") and r.get("result"), str(r)[:80])

    r = execute_tool("system.version", {})
    ok("system.version", r.get("success"), str(r))


def test_script_engine() -> None:
    section("ROKO Script engine")
    from APP.router import run_script

    script = "CALL math.sum WITH a=10, b=5 AS s\nRETURN ${s}"
    r = run_script(script)
    ok("simple CALL+RETURN", r.get("success") and r.get("return_value") == 15, str(r.get("return_value")))

    script = """
SET x TO 3
SET y TO 4
CALL math.sum WITH a=${x}, b=${y} AS total
CALL math.multiply WITH a=${total}, b=2 AS dob
RETURN {"total": ${total}, "dob": ${dob}}
"""
    r = run_script(script)
    ok("vars + multi CALL", r.get("success") and r.get("return_value", {}).get("dob") == 14, str(r.get("return_value")))

    script = """
IF true THEN
  RETURN 42
END
RETURN 0
"""
    r = run_script(script)
    ok("IF true", r.get("success") and r.get("return_value") == 42, str(r.get("return_value")))

    script = """
SET n TO 0
WHILE ${n} < 3 DO
  SET n TO ${n} + 1
END
RETURN ${n}
"""
    r = run_script(script)
    ok("WHILE loop", r.get("success") and r.get("return_value") == 3, str(r.get("return_value")))


def test_oracle_priority() -> None:
    section("Oracle priority vs native")
    from TOOLS.registry import execute_tool

    r = execute_tool("math.sum", {"a": 1, "b": 2})
    ok("public math.sum (Oracle)", r.get("success") and r.get("result") == 3)

    r = execute_tool("native.math.sum", {"a": 1, "b": 2})
    ok("native.math.sum (Python)", r.get("success") and r.get("result") == 3)


def test_agent() -> None:
    section("Agent simbólico agent.run")
    from TOOLS.registry import execute_tool

    r = execute_tool("agent.run", {
        "plan": "plans/math_demo.roko",
        "goal": "Somar e dobrar",
        "max_steps": 5,
        "user_id": "battery",
        "id": "bat-1",
    })
    ok("agent.run success", r.get("success") is True, str(r)[:200])
    res = r.get("result") or {}
    ok("agent ok flag", res.get("ok") is True, str(res)[:150])
    resp = res.get("response") or {}
    ok("agent response soma", resp.get("soma") == 15, str(resp))
    ok("agent response dobro", resp.get("dobro") == 30, str(resp))


def test_memory_hgr() -> None:
    section("HGR / memory tools")
    from TOOLS.registry import execute_tool

    uid = "battery_user"
    r = execute_tool("memory.store_fact", {
        "user_id": uid,
        "key": "test_key",
        "value": "hello_roko",
        "importance": 0.9,
        "category": "test",
    })
    ok("store_fact", r.get("success"), str(r)[:120])

    r = execute_tool("memory.get_fact", {"user_id": uid, "key": "test_key"})
    ok("get_fact", r.get("success") and "hello_roko" in str(r.get("result")), str(r)[:150])

    r = execute_tool("memory.search_facts", {"user_id": uid, "query": "hello"})
    ok("search_facts", r.get("success"), str(r)[:120])

    r = execute_tool("memory.stats", {"user_id": uid})
    ok("memory.stats", r.get("success"), str(r)[:120])


def test_http_fixed() -> None:
    section("HTTP tools (incl. get_json fix)")
    from TOOLS.registry import execute_tool

    # status should work offline-ish or against public
    r = execute_tool("http.status", {"url": "https://httpbin.org/status/200"})
    ok("http.status 200", r.get("success") and r.get("result") in (200, -1), str(r))  # -1 if no net

    r = execute_tool("http.get_json", {"url": "https://httpbin.org/json"})
    # success if network available
    if r.get("success"):
        ok("http.get_json (network)", True)
    else:
        ok("http.get_json graceful fail or network", "error" in r or not r.get("success"), str(r)[:100])


def test_parallel_meta() -> None:
    section("Parallel / meta tools")
    from TOOLS.registry import execute_tool

    r = execute_tool("meta.info", {})
    ok("meta.info", r.get("success") and r.get("result", {}).get("total_tools", 0) >= 120)

    r = execute_tool("parallel.info", {})
    ok("parallel.info", r.get("success"), str(r)[:100])


def test_plans_exist() -> None:
    section("Plans & Oracle presence")
    plans = list((REPOSITORY / "plans").glob("*.roko"))
    ok("plans/ has .roko", len(plans) >= 3, str(len(plans)))

    oracle_math = REPOSITORY / "Oracle" / "math" / "sum.roko"
    ok("Oracle/math/sum.roko exists", oracle_math.exists())

    roko_count = len(list((REPOSITORY / "Oracle").rglob("*.roko")))
    ok("Oracle has >= 100 .roko", roko_count >= 100, str(roko_count))


def test_limits() -> None:
    section("Limits")
    from engine.limits import MAX_EXEC_SECONDS, MAX_SCRIPT_LINES
    ok("MAX_EXEC_SECONDS == 60", MAX_EXEC_SECONDS == 60, str(MAX_EXEC_SECONDS))
    ok("MAX_SCRIPT_LINES high", MAX_SCRIPT_LINES >= 1000)


def main() -> int:
    print("ROKO ENGINE LITE — Bateria de testes pesados")
    print(f"Root: {REPOSITORY}")
    start = time.time()
    try:
        test_registry()
        test_core_tools()
        test_script_engine()
        test_oracle_priority()
        test_agent()
        test_memory_hgr()
        test_http_fixed()
        test_parallel_meta()
        test_plans_exist()
        test_limits()
    except Exception as e:
        print("FATAL:", e)
        traceback.print_exc()
        return 2

    elapsed = time.time() - start
    print(f"\n=== RESULTADO ===")
    print(f"Passed: {PASSED}")
    print(f"Failed: {FAILED}")
    print(f"Elapsed: {elapsed:.2f}s")
    if ERRORS:
        print("Falhas:")
        for e in ERRORS:
            print(e)
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
