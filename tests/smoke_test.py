"""Release smoke checks for the modular ROKO ENGINE LITE runtime."""

import asyncio
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

from api import app  # noqa: E402
from router import run_script  # noqa: E402
from tools import execute_tool, meta_info  # noqa: E402


def test_runtime() -> None:
    info = meta_info()
    assert info["total_tools"] == 92, info
    assert info["version"] == "2.1.0", info

    tool_result = execute_tool("math.sum", {"a": 7, "b": 8})
    assert tool_result == {"success": True, "result": 15.0}, tool_result

    script = "SET a TO 7\nSET b TO 8\nCALL math.sum WITH a=${a}, b=${b} AS total\nRETURN total"
    execution = run_script(script)
    assert execution["success"] is True, execution
    assert execution["return_value"] == 15.0, execution

    sample = (REPOSITORY / "examples" / "semantic_router.roko").read_text(encoding="utf-8")
    routed = run_script(sample)
    assert routed["success"] is True, routed
    assert routed["return_value"]["tool_escolhida"] == "math.sum", routed
    assert routed["return_value"]["resultado"] == 15.0, routed


async def test_http() -> None:
    client = app.test_client()

    root = await client.get("/")
    assert root.status_code == 200
    root_payload = await root.get_json()
    assert root_payload["version"] == "2.1.0", root_payload
    assert root_payload["total_tools"] == 92, root_payload

    tool = await client.post("/tool/math.sum", json={"a": 7, "b": 8})
    assert tool.status_code == 200
    tool_payload = await tool.get_json()
    assert tool_payload["result"] == 15.0, tool_payload

    script = await client.post(
        "/script/execute",
        json={"script": "CALL math.sum WITH a=7, b=8 AS total\nRETURN total"},
    )
    assert script.status_code == 200
    script_payload = await script.get_json()
    assert script_payload["return_value"] == 15.0, script_payload

    quick = await client.get("/math/sum?a=7&b=8")
    assert quick.status_code == 200
    quick_payload = await quick.get_json()
    assert quick_payload["result"] == 15.0, quick_payload

    validation = await client.post("/script/validate", json={"script": "IF true THEN\nRETURN 1\nEND"})
    assert validation.status_code == 200
    validation_payload = await validation.get_json()
    assert validation_payload["valid"] is True, validation_payload

    streaming = await client.post("/script/stream", json={"script": "RETURN 1"})
    assert streaming.status_code == 200
    stream_body = (await streaming.get_data()).decode("utf-8")
    assert "event: start" in stream_body, stream_body
    assert "event: done" in stream_body, stream_body


if __name__ == "__main__":
    test_runtime()
    asyncio.run(test_http())
    print("ROKO integration smoke checks passed")
