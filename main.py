"""Backward-compatible entry point for the modular ROKO ENGINE LITE API."""

import os

from api import app


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8989))
    debug_mode = os.environ.get("ROKO_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug_mode)
