from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel
from backend.app.schemas.auth import UserResponse, InvestorProfileSchema
from backend.app.schemas.venture import VentureResponse

class InvestorDashboardResponse(CamelModel):
    user: UserResponse
    capital_deployed_cents: int
    portfolio_count: int
    unread_updates_count: int
    holdings: List[Dict[str, Any]]
    recent_milestones: List[Dict[str, Any]]

class InvestmentDetailResponse(CamelModel):
    id: str
    investor_id: str
    venture_id: str
    venture_name: str
    venture_sector: str
    venture_stage: str
    instrument_type: str
    instrument_label: str
    principal_cents: int
    val_cap_cents: int
    discount_pct: float
    equity_pct: float
    contract_addr: str
    signed_on: str
    status: str

class MilestoneUpdateResponse(CamelModel):
    id: str
    venture_id: str
    venture_name: str
    headline: str
    body: str
    stage_label: str
    tag: str
    merkle_proof: str
    deliverables: List[str]
    metrics: Dict[str, Any]
    published_at: Optional[datetime.datetime] = None
    is_read: bool = False

class InvestorSettingsUpdate(CamelModel):
    tier: Optional[str] = None
    wallet_address: Optional[str] = None
    preferred_sectors: Optional[List[str]] = None
    instant_alerts: Optional[bool] = None
    weekly_digest: Optional[bool] = None

class DisclosureRequestCreate(CamelModel):
    venture_id: str

class DisclosureRequestResponse(CamelModel):
    id: str
    investor_id: str
    venture_id: str
    status: str
    created_at: Optional[datetime.datetime] = None
