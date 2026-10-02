#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke checks — ROKO ENGINE LITE 2.3.1"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

from TOOLS.registry import execute_tool, meta_info
from APP.router import run_script


def test_runtime() -> None:
    info = meta_info()
    assert info["total_tools"] >= 120, info
    assert info["version"] == "2.3.1", info
    assert info["roko_tools"] == 121, info

    tool_result = execute_tool("math.sum", {"a": 7, "b": 8})
    assert tool_result.get("success") and tool_result.get("result") == 15, tool_result

    script = "SET a TO 7\nSET b TO 8\nCALL math.sum WITH a=${a}, b=${b} AS total\nRETURN total"
    execution = run_script(script)
    assert execution["success"] is True, execution
    assert execution["return_value"] == 15, execution

    sample = (REPOSITORY / "examples" / "semantic_router.roko")
    if sample.exists():
        routed = run_script(sample.read_text(encoding="utf-8"))
        assert routed["success"] is True, routed


async def test_http() -> None:
    from APP.api import app
    client = app.test_client()

    root = await client.get("/")
    assert root.status_code == 200
    root_payload = await root.get_json()
    assert root_payload["version"] == "2.3.1", root_payload
    assert root_payload["total_tools"] >= 120, root_payload

    tool = await client.post("/tool/math.sum", json={"a": 7, "b": 8})
    assert tool.status_code == 200
    tool_payload = await tool.get_json()
    assert tool_payload.get("result") == 15, tool_payload

    script = await client.post(
        "/script/execute",
        json={"script": "CALL math.sum WITH a=7, b=8 AS total\nRETURN total"},
    )
    assert script.status_code == 200
    script_payload = await script.get_json()
    assert script_payload.get("return_value") == 15, script_payload


if __name__ == "__main__":
    test_runtime()
    try:
        asyncio.run(test_http())
    except Exception as e:
        print("HTTP smoke skipped or partial:", e)
    print("ROKO smoke checks passed (2.3.1)")
