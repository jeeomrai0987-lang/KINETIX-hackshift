from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel

class CapTableEntryResponse(CamelModel):
    id: str
    venture_id: str
    holder_user_id: Optional[str] = None
    holder_label: str
    equity_pct: float
    kind: str
    vested_pct: float

class CapTableResponse(CamelModel):
    venture_id: str
    total_equity_pct: float
    total_equity: Optional[float] = None
    entries: List[CapTableEntryResponse]

class TransactionResponse(CamelModel):
    id: str
    venture_id: str
    occurred_on: str
    description: str
    category: str
    amount_cents: int
    proof_hash: str
    created_at: Optional[datetime.datetime] = None

class FinancialSnapshotResponse(CamelModel):
    id: str
    venture_id: str
    month: str
    burn_cents: int
    revenue_cents: int
    cash_cents: int

class FinancialsOverviewResponse(CamelModel):
    venture_id: str
    range: str
    burn_cents: int
    monthly_burn_cents: Optional[int] = None
    revenue_cents: int
    cash_cents: int
    runway_months: int
    snapshots: List[FinancialSnapshotResponse]

class FundingOpportunityResponse(CamelModel):
    id: str
    name: str
    category: str
    check_min_cents: int
    check_max_cents: int
    structure: str
    tags: List[str]
    timeline: str
    base_fit_pct: float
    status: Optional[str] = "available"  # available, requested, under_review

class FundingRequestCreate(CamelModel):
    note: Optional[str] = None

class FundingRequestResponse(CamelModel):
    id: str
    venture_id: str
    funding_opportunity_id: str
    status: str
    created_at: Optional[datetime.datetime] = None
