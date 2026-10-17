from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel

class MatchResponse(CamelModel):
    id: str
    venture_id: str
    role_id: str
    role_title: Optional[str] = None
    worker_id: str
    candidate_code: str
    synergy_score: int
    fit_details: Dict[str, Any] = {}
    status: str
    skills: List[str] = []
    experience_level: Optional[str] = None
    percentile: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    # NOTE: Strictly no real name/email/phone here for unaccepted candidates!

class InviteRequest(CamelModel):
    equity_pct: float
    terms: Optional[str] = "Standard 4-year vesting with 1-year cliff."
    message: Optional[str] = None

class InvitationResponse(CamelModel):
    id: str
    venture_id: str
    venture_name: Optional[str] = None
    role_id: str
    role_title: Optional[str] = None
    worker_id: str
    candidate_code: Optional[str] = None
    # Only populated if accepted
    worker_name: Optional[str] = None
    worker_email: Optional[str] = None
    worker_avatar_url: Optional[str] = None
    equity_pct: float
    terms: Optional[str] = None
    message: Optional[str] = None
    status: str
    responded_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
