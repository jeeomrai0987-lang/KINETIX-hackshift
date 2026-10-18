import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base, TimestampMixin, utcnow

def generate_id(prefix: str = "inv") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class InvestorProfile(Base, TimestampMixin):
    __tablename__ = "investor_profiles"
    __table_args__ = (
        CheckConstraint("accreditation_status IN ('pending', 'verified', 'expired')", name="chk_accreditation_status"),
    )

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    wallet_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferred_sectors: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    instant_alerts: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weekly_digest: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    accreditation_status: Mapped[str] = mapped_column(String(20), default="verified", nullable=False)  # pending, verified, expired
    accreditation_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])


class Investment(Base, TimestampMixin):
    __tablename__ = "investments"
    __table_args__ = (
        CheckConstraint("instrument_type IN ('safe', 'grant')", name="chk_investment_instrument"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("invst"))
    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="RESTRICT"), index=True, nullable=False)
    instrument_type: Mapped[str] = mapped_column(String(20), nullable=False)  # safe, grant
    instrument_label: Mapped[str] = mapped_column(String(100), nullable=False)
    principal_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    val_cap_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    contract_addr: Mapped[str] = mapped_column(String(100), nullable=False)
    signed_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True, nullable=False)

    # Relationships
    investor: Mapped["User"] = relationship("User", foreign_keys=[investor_id])
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])


class MilestoneUpdate(Base):
    __tablename__ = "milestone_updates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("mls"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    headline: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    stage_label: Mapped[str] = mapped_column(String(100), nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)
    merkle_proof: Mapped[str] = mapped_column(String(100), nullable=False)
    deliverables: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])
    reads: Mapped[List["MilestoneRead"]] = relationship("MilestoneRead", back_populates="update", cascade="all, delete-orphan")


class MilestoneRead(Base):
    __tablename__ = "milestone_reads"

    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    update_id: Mapped[str] = mapped_column(String(36), ForeignKey("milestone_updates.id", ondelete="CASCADE"), primary_key=True)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    investor: Mapped["User"] = relationship("User", foreign_keys=[investor_id])
    update: Mapped["MilestoneUpdate"] = relationship("MilestoneUpdate", back_populates="reads")


class DisclosureRequest(Base, TimestampMixin):
    __tablename__ = "disclosure_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("dsc"))
    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True, nullable=False)

    # Relationships
    investor: Mapped["User"] = relationship("User", foreign_keys=[investor_id])
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])
