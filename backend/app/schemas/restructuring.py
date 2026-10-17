from typing import Optional
import datetime
from backend.app.schemas.base import CamelModel

class RestructuringExecuteRequest(CamelModel):
    type: str
    from_user_id: Optional[str] = None
    to_user_id: Optional[str] = None
    equity_delta_pct: float
    stage: Optional[str] = "Approved"
    note: Optional[str] = None

class RestructuringEventResponse(CamelModel):
    id: str
    venture_id: str
    type: str
    from_user_id: Optional[str] = None
    from_user_name: Optional[str] = None
    to_user_id: Optional[str] = None
    to_user_name: Optional[str] = None
    equity_delta_pct: float
    stage: str
    note: Optional[str] = None
    executed_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
