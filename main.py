# ROKO ENGINE LITE
# Entry point principal

import os
from quart import Quart, jsonify
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")

VERSION = "2.1.0"

@app.route("/")
async def index():
    return jsonify({
        "name": "ROKO ENGINE LITE",
        "version": VERSION,
        "status": "running"
    })

@app.route("/health")
async def health():
    return jsonify({"status": "ok"})

@app.route("/version")
async def version():
    return jsonify({"version": VERSION})

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
