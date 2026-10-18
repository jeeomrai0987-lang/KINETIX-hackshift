import uuid
import datetime
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from backend.app.db import models

def log_audit(
    db: Session,
    actor_id: str,
    action: str,
    entity: str,
    entity_id: str,
    payload: Optional[Dict[str, Any]] = None
) -> models.AuditLog:
    """
    Writes an audit_log record for state changes.
    Meets Section 6 Rule 5 of docs/SHARED_CONTRACT.md.
    """
    log_entry = models.AuditLog(
        id=f"aud_{uuid.uuid4().hex[:12]}",
        actor_id=actor_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        payload=payload or {},
        created_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    )
    db.add(log_entry)
    return log_entry
