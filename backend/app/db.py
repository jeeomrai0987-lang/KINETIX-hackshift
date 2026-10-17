"""
Database session bridge.
Per docs/SHARED_CONTRACT.md:
"The backend imports only from database via from database.session import get_db, SessionLocal and from database import models. Nothing else crosses the boundary."
If the database package is not present yet (Person A/C hasn't pushed it),
this module falls back to backend.db_stub.
"""

try:
    from database.session import get_db, SessionLocal
    from database import models
    HAVE_DATABASE_PACKAGE = True
except (ImportError, ModuleNotFoundError):
    from backend.db_stub import get_db, SessionLocal, models
    HAVE_DATABASE_PACKAGE = False

__all__ = ["get_db", "SessionLocal", "models", "HAVE_DATABASE_PACKAGE"]
