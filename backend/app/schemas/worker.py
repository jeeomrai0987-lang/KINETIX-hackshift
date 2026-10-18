from typing import Optional, List
from backend.app.schemas.common import CamelModel


class WorkerProfileUpdate(CamelModel):
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
    weekly_availability_hours: Optional[int] = None
    phone: Optional[str] = None
    github_url: Optional[str] = None


class OpportunityApplyRequest(CamelModel):
    blind_token: Optional[str] = None
