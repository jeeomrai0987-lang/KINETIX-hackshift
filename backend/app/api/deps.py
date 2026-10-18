from typing import Optional, List, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.core.security import decode_access_token

security = HTTPBearer(auto_error=False)

def get_db():
    try:
        from database.session import get_db as _get_db
        yield from _get_db()
    except (ImportError, ModuleNotFoundError):
        yield None

def get_model(name: str):
    try:
        from database import models
        if hasattr(models, name):
            return getattr(models, name)
    except (ImportError, ModuleNotFoundError):
        pass

    # Fallback to direct modules if __init__.py hasn't re-exported yet
    try:
        from database.models import core, venture, finance, investor, worker_profile, worker_activity
        for mod in (core, venture, finance, investor, worker_profile, worker_activity):
            if hasattr(mod, name):
                return getattr(mod, name)
    except (ImportError, ModuleNotFoundError):
        pass

    return None

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "unauthorized", "message": "Missing bearer token"}},
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "invalid_token", "message": "Invalid or expired access token"}},
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "invalid_token", "message": "Token missing subject"}},
        )

    User = get_model("User")
    if User is not None and db is not None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": {"code": "user_not_found", "message": "User not found"}},
            )
        return user

    # Pre-A1 mock / fallback user object
    class TransientUser:
        def __init__(self, uid: str, role: str, email: str):
            self.id = uid
            self.role = role
            self.email = email
            self.name = payload.get("name", "User")
            self.title = None
            self.avatar_url = None
            self.node_id = None
            self.verified = True
            self.cohort_id = None
            self.worker_profile = None
            self.investor_profile = None
            self.created_at = None

    return TransientUser(user_id, payload.get("role", "founder"), payload.get("email", ""))

def require_role(*roles: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": {"code": "forbidden", "message": f"Requires one of roles: {', '.join(roles)}"}},
            )
        return current_user
    return role_checker
