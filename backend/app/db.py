"""
Database session bridge.
Per docs/SHARED_CONTRACT.md:
"The backend imports only from database via from database.session import get_db, SessionLocal and from database import models. Nothing else crosses the boundary."
"""

try:
    from database.session import get_db, SessionLocal
    from database import models
except (ImportError, ModuleNotFoundError):
    SessionLocal = None

    class _ModelsFallback:
        def __getattr__(self, name: str):
            from typing import Any
            return Any

    models = _ModelsFallback()

    def get_db():
        yield None

__all__ = ["get_db", "SessionLocal", "models"]
