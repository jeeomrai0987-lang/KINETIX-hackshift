from typing import Optional, List
from backend.app.schemas.common import CamelModel


class RegisterRequest(CamelModel):
    name: str
    email: str
    password: str
    role: str = "founder"  # founder, investor, worker
    title: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    experience_level: Optional[str] = "mid"
    whatsapp_enabled: Optional[bool] = True


class LoginRequest(CamelModel):
    email: str
    password: str


class UserResponse(CamelModel):
    id: str
    email: str
    name: str
    role: str
    title: Optional[str] = None
    avatar_url: Optional[str] = None
    node_id: Optional[str] = None
    verified: bool = True
    cohort_id: Optional[str] = None


class AuthResponse(CamelModel):
    token: str
    user: UserResponse
