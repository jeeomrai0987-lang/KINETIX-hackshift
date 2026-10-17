from typing import Optional, List, Any
import datetime
from pydantic import EmailStr, Field
from backend.app.schemas.base import CamelModel

class RegisterRequest(CamelModel):
    name: str
    email: EmailStr
    password: str
    role: str = Field(default="founder")  # founder, worker, investor
    title: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    experience_level: Optional[str] = "mid"
    whatsapp_enabled: Optional[bool] = False

class LoginRequest(CamelModel):
    email: EmailStr
    password: str

class WorkerProfileSchema(CamelModel):
    experience_level: str
    skills: List[str]
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    phone: Optional[str] = None
    whatsapp_enabled: bool = False
    cloaked: bool = True
    weekly_availability_hours: int = 40
    percentile: int = 96

class InvestorProfileSchema(CamelModel):
    tier: str
    wallet_address: Optional[str] = None
    preferred_sectors: List[str]
    instant_alerts: bool = True
    weekly_digest: bool = True
    accreditation_status: str
    accreditation_expires_at: Optional[datetime.datetime] = None

class UserResponse(CamelModel):
    id: str
    name: str
    email: str
    role: str
    title: Optional[str] = None
    avatar_url: Optional[str] = None
    node_id: Optional[str] = None
    verified: bool = False
    cohort_id: Optional[str] = None
    worker_profile: Optional[WorkerProfileSchema] = None
    investor_profile: Optional[InvestorProfileSchema] = None
    created_at: Optional[datetime.datetime] = None

class AuthResponse(CamelModel):
    token: str
    user: UserResponse
