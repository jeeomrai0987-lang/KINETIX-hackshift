from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel
from backend.app.schemas.auth import UserResponse, WorkerProfileSchema
from backend.app.schemas.match import InvitationResponse
from backend.app.schemas.challenge import ProofReportResponse

class WorkerDashboardResponse(CamelModel):
    user: UserResponse
    percentile: int
    active_challenges_count: int
    pending_invitations_count: int
    proof_reports_count: int
    telemetry: Dict[str, Any]

class WorkerProfileUpdate(CamelModel):
    name: Optional[str] = None
    title: Optional[str] = None
    experience_level: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None
    phone: Optional[str] = None
    whatsapp_enabled: Optional[bool] = None
    cloaked: Optional[bool] = None
    weekly_availability_hours: Optional[int] = None

class WorkerSettingsUpdate(CamelModel):
    cloaked: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    phone: Optional[str] = None
    weekly_availability_hours: Optional[int] = None

class WorkerOpportunity(CamelModel):
    role_id: str
    venture_id: str
    venture_name: str
    venture_sector: str
    role_title: str
    description: str
    equity_pct: float
    requirements: List[str]
    blind_token: str
    synergy_score: int
    applied: bool = False
