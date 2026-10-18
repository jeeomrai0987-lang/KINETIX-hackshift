import json
import hashlib
import bcrypt
from datetime import datetime, timezone
from typing import Any, Dict, Type
from sqlalchemy.orm import Session

SHARED_DEMO_PASSWORD = "Demo#2026"

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def hash_password(password: str = SHARED_DEMO_PASSWORD) -> str:
    """Hashes a password with bcrypt, returning a decoded UTF-8 string."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def canonical_hash(payload: Dict[str, Any]) -> str:
    """Computes a deterministic SHA-256 hash (0x-prefixed) of a canonical JSON payload."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def upsert(db: Session, model: Type[Any], key_attrs: Dict[str, Any], defaults: Dict[str, Any]) -> Any:
    """Helper to insert or update a record matching key_attrs."""
    instance = db.query(model).filter_by(**key_attrs).first()
    if instance:
        for k, v in defaults.items():
            setattr(instance, k, v)
    else:
        params = {**key_attrs, **defaults}
        instance = model(**params)
        db.add(instance)
    return instance
