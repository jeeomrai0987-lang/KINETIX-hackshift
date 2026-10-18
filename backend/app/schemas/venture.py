from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel

class VentureCreate(CamelModel):
    name: str
    thesis: str
    sector: str
    stage: Optional[str] = "Sprint 3 / Proof-of-Work"
    constraints: Optional[Dict[str, Any]] = None

class VentureUpdate(CamelModel):
    name: Optional[str] = None
    thesis: Optional[str] = None
    sector: Optional[str] = None
    stage: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    runway_months: Optional[int] = None
    mrr_cents: Optional[int] = None
    raised_cents: Optional[int] = None

class SquadRoleSchema(CamelModel):
    id: str
    venture_id: str
    title: str
    description: Optional[str] = None
    equity_pct: float
    status: str
    filled_by_user_id: Optional[str] = None
    requirements: List[str] = []
    created_at: Optional[datetime.datetime] = None

class VentureResponse(CamelModel):
    id: str
    founder_id: str
    cohort_id: Optional[str] = None
    name: str
    thesis: str
    sector: str
    stage: str
    clarity_score: int
    constraints: Dict[str, Any] = {}
    raised_cents: int
    runway_months: int
    mrr_cents: int
    status: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

class DecomposeRequest(CamelModel):
    thesis: str

class SkillWeight(CamelModel):
    skill: str
    weight: float = 1.0

class BlueprintRole(CamelModel):
    title: str
    description: str
    equity_pct: float
    requirements: List[Any] = []
    required_skills: Optional[List[Any]] = None
    min_experience: Optional[str] = "senior"

class DecomposeResponse(CamelModel):
    thesis: str
    constraints: Dict[str, Any]
    blueprint: List[BlueprintRole]
    roles: Optional[List[BlueprintRole]] = None
    clarity_score: int
    source: str = "fallback"  # "gemini" | "fallback"
    latency_ms: int = 0

class BlueprintApproveRequest(CamelModel):
    roles: Optional[List[BlueprintRole]] = None
    blueprint: Optional[List[BlueprintRole]] = None

class VentureDashboardResponse(CamelModel):
    venture: VentureResponse
    squad_synergy: int
    runway: str
    sprint_clock: Dict[str, Any]
    roster: List[Dict[str, Any]]
    cohort_feed: List[Dict[str, Any]]
