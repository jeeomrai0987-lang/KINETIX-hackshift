import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    DateTime,
    JSON,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base, TimestampMixin, utcnow

def generate_id(prefix: str = "fin") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class CapTableEntry(Base, TimestampMixin):
    __tablename__ = "cap_table_entries"
    __table_args__ = (
        CheckConstraint("kind IN ('founder', 'cofounder', 'reserve', 'option_pool', 'investor_safe')", name="chk_cap_kind"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("cap"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    holder_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    holder_label: Mapped[str] = mapped_column(String(100), nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    kind: Mapped[str] = mapped_column(String(30), nullable=False)  # founder, cofounder, reserve, option_pool, investor_safe
    vested_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])
    holder_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[holder_user_id])


class RestructuringEvent(Base):
    __tablename__ = "restructuring_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("rst"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    from_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    to_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    equity_delta_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])
    from_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[from_user_id])
    to_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[to_user_id])


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("category IN ('infrastructure', 'revenue', 'payroll', 'legal', 'other')", name="chk_txn_category"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("txn"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    occurred_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # infrastructure, revenue, payroll, legal, other
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)  # signed int cents
    proof_hash: Mapped[str] = mapped_column(String(66), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])


class FinancialSnapshot(Base):
    __tablename__ = "financial_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("snp"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    burn_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    revenue_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cash_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])


class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"
    __table_args__ = (
        CheckConstraint("category IN ('syndicate', 'micro_vc', 'grant')", name="chk_funding_opp_category"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("opp"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # syndicate, micro_vc, grant
    check_min_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    check_max_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    structure: Mapped[str] = mapped_column(String(100), nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    timeline: Mapped[str] = mapped_column(String(50), nullable=False)
    base_fit_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    requests: Mapped[List["FundingRequest"]] = relationship("FundingRequest", back_populates="opportunity", cascade="all, delete-orphan")


class FundingRequest(Base, TimestampMixin):
    __tablename__ = "funding_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("fnr"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    funding_opportunity_id: Mapped[str] = mapped_column(String(36), ForeignKey("funding_opportunities.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", foreign_keys=[venture_id])
    opportunity: Mapped["FundingOpportunity"] = relationship("FundingOpportunity", back_populates="requests")
