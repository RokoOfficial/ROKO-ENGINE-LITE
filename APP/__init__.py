"""Camada de aplicação (API HTTP + facade)."""

# Imports leves (sem Quart) para uso em testes e no motor
from .router import (
    run_script,
    validate_script,
    APP_NAME,
    APP_VERSION,
    API_VERSION,
)

__all__ = [
    "run_script",
    "validate_script",
    "APP_NAME",
    "APP_VERSION",
    "API_VERSION",
]


def get_app():
    """Import lazy do app Quart (só quando a API for realmente usada)."""
    from .api import app
    return app
