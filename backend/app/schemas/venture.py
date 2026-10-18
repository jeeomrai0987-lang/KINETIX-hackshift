from typing import Optional, List, Dict, Any
from backend.app.schemas.common import CamelModel


class DecomposeRequest(CamelModel):
    thesis: str


class DecomposeResponse(CamelModel):
    venture_id: str
    clarity_score: int
    core_modules: List[Dict[str, Any]]
    squad_blueprint: List[Dict[str, Any]]
    constraints: Dict[str, Any]


class BlueprintApproveRequest(CamelModel):
    roles: List[Dict[str, Any]]


class ScoreRequest(CamelModel):
    vector_scores: Dict[str, float]
    score: Optional[float] = None
    reviewer_verdict: Optional[str] = "Attested"


class SignRequest(CamelModel):
    signature_note: Optional[str] = "Signed on protocol ledger"


class RestructureExecuteRequest(CamelModel):
    candidate_id: Optional[str] = None
    role_id: Optional[str] = None
    equity_pct: Optional[float] = None
    note: Optional[str] = None


class FundingRequestCreate(CamelModel):
    funding_opportunity_id: str
