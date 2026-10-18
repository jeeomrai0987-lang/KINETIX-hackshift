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
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base, TimestampMixin, utcnow

def generate_id(prefix: str = "ven") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class Venture(Base, TimestampMixin):
    __tablename__ = "ventures"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("ven"))
    founder_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    cohort_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    thesis: Mapped[str] = mapped_column(Text, nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    clarity_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    constraints: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)  # latency, compliance, squadSize...
    raised_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    runway_months: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    mrr_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True, nullable=False)

    # Relationships (string references)
    founder: Mapped["User"] = relationship("User", foreign_keys=[founder_id])
    cohort: Mapped[Optional["Cohort"]] = relationship("Cohort", foreign_keys=[cohort_id])
    squad_roles: Mapped[List["SquadRole"]] = relationship("SquadRole", back_populates="venture", cascade="all, delete-orphan")
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", back_populates="venture", cascade="all, delete-orphan")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="venture", cascade="all, delete-orphan")


class SquadRole(Base, TimestampMixin):
    __tablename__ = "squad_roles"
    __table_args__ = (
        CheckConstraint("status IN ('filled', 'vacant', 'reserved')", name="chk_squad_role_status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("rol"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="vacant", index=True, nullable=False)  # filled, vacant, reserved
    filled_by_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    requirements: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", back_populates="squad_roles")
    filled_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[filled_by_user_id])
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", back_populates="role", cascade="all, delete-orphan")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="role", cascade="all, delete-orphan")


class Challenge(Base):
    __tablename__ = "challenges"
    __table_args__ = (
        CheckConstraint("status IN ('open', 'closed')", name="chk_challenge_status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("chl"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    duration_hours: Mapped[int] = mapped_column(Integer, default=48, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True, nullable=False)  # open, closed
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", back_populates="challenges")
    role: Mapped["SquadRole"] = relationship("SquadRole", back_populates="challenges")


class Match(Base, TimestampMixin):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_matches_role_worker"),
        CheckConstraint("status IN ('suggested', 'invited', 'declined')", name="chk_match_status"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("mat"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    candidate_code: Mapped[str] = mapped_column(String(50), nullable=False)
    synergy_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fit_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="suggested", index=True, nullable=False)  # suggested, invited, declined

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", back_populates="matches")
    role: Mapped["SquadRole"] = relationship("SquadRole", back_populates="matches")
    worker: Mapped["User"] = relationship("User", foreign_keys=[worker_id])
