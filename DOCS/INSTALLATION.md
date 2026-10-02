# Installation and configuration

## Prerequisites

Install **Python 3.10 or newer** and a current `pip`. The runtime has four direct Python dependencies: Quart and Quart-CORS for the web service, Requests for HTTP tools, and Werkzeug for filename sanitization.

| Dependency | Declared requirement | Used by |
|---|---:|---|
| `quart` | `>=0.19` | HTTP application and server |
| `quart-cors` | `>=0.7` | Cross-origin response configuration |
| `requests` | `>=2.31` | `http.*` tools |
| `werkzeug` | `>=3.0` | Safe `.roko` filename handling |

## Local setup

Clone the repository, create a virtual environment, and install the locked project requirements.

```bash
git clone https://github.com/RokoOfficial/ROKO-ENGINE-LITE.git
cd ROKO-ENGINE-LITE
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the backward-compatible entry point for local development.

```bash
python main.py
```

The modular HTTP module can also be executed directly.

```bash
python api.py
```

Both commands load the same Quart `app` object. A default process listens on all network interfaces at port `8989`; verify it with:

```bash
curl -sS http://127.0.0.1:8989/health
```

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `HOST` | `0.0.0.0` | Interface to which the server binds |
| `PORT` | `8989` | TCP port used by the server |
| `ROKO_DEBUG` | `false` | Enables Quart debug mode when set to `true` case-insensitively |
| `ROKO_SECRET_KEY` | Built-in development fallback | Secret used by the Quart application; set a unique value outside local development |

A local-only development process can be started with the following command.

```bash
HOST=127.0.0.1 PORT=8989 ROKO_DEBUG=true ROKO_SECRET_KEY='development-only-secret' python main.py
```

## Production process guidance

For a production deployment, run the ASGI application behind an ASGI server and a reverse proxy rather than the built-in development server. The application object is exposed at `api:app`, so a typical ASGI process command is:

```bash
hypercorn api:app --bind 127.0.0.1:8989
```

Place the process behind TLS termination, authenticate the callers that may execute tools or scripts, set a non-default `ROKO_SECRET_KEY`, and restrict CORS origins. The source currently permits every origin by default; replace that development-oriented policy in `api.py` with a trusted-origin allowlist before public exposure.

| Deployment concern | Recommended control |
|---|---|
| Network exposure | Bind privately or protect the service behind a reverse proxy |
| Transport | Terminate TLS at the proxy and redirect insecure requests |
| Authentication | Require identity before script, tool, or file operations |
| CORS | Replace `*` with the known frontend origins |
| Secret | Provide a unique `ROKO_SECRET_KEY` through the environment |
| File persistence | Mount or back up the runtime's `uploads/` directory if retained scripts matter |
| Outbound HTTP tools | Apply egress filtering and target allowlists when scripts are not fully trusted |

## Upgrade procedure

Stop the service, pull the desired revision, refresh the virtual environment dependencies, review the changelog, and run the validation steps before restarting the process.

```bash
git pull --ff-only
python -m pip install -r requirements.txt
python -m py_compile api.py router.py roko.py tools.py main.py
python main.py
```

The final command should be run under the same environment configuration that the deployment uses. Consult [Validation](VALIDATION.md) for behavior-level checks and [Security](SECURITY.md) for the operational risk model.
