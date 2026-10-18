from typing import Optional, List
from backend.app.schemas.common import CamelModel


class InvestorSettingsUpdate(CamelModel):
    preferred_sectors: Optional[List[str]] = None
    wallet_address: Optional[str] = None
    instant_alerts: Optional[bool] = None
    weekly_digest: Optional[bool] = None


class DisclosureRequestCreate(CamelModel):
    venture_id: str
