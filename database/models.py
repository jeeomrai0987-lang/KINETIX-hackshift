import uuid
from datetime import datetime, timezone
from typing import Optional, List, Any, Dict
from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .session import Base

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def generate_id(prefix: str = "ent") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class Cohort(Base):
    __tablename__ = "cohorts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("coh"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    batch_no: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="cohort")
    ventures: Mapped[List["Venture"]] = relationship("Venture", back_populates="cohort")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("usr"))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # founder, investor, worker
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    node_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    cohort_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    cohort: Mapped[Optional["Cohort"]] = relationship("Cohort", back_populates="users")
    worker_profile: Mapped[Optional["WorkerProfile"]] = relationship("WorkerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    investor_profile: Mapped[Optional["InvestorProfile"]] = relationship("InvestorProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    ventures_founded: Mapped[List["Venture"]] = relationship("Venture", back_populates="founder")


class WorkerProfile(Base):
    __tablename__ = "worker_profiles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    experience_level: Mapped[str] = mapped_column(String(20), default="senior")  # junior, mid, senior, founding
    skills: Mapped[List[str]] = mapped_column(JSON, default=list)
    portfolio_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    whatsapp_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    cloaked: Mapped[bool] = mapped_column(Boolean, default=True)
    weekly_availability_hours: Mapped[int] = mapped_column(Integer, default=40)
    percentile: Mapped[float] = mapped_column(Float, default=95.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user: Mapped["User"] = relationship("User", back_populates="worker_profile")


class InvestorProfile(Base):
    __tablename__ = "investor_profiles"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    wallet_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferred_sectors: Mapped[List[str]] = mapped_column(JSON, default=list)
    instant_alerts: Mapped[bool] = mapped_column(Boolean, default=True)
    weekly_digest: Mapped[bool] = mapped_column(Boolean, default=True)
    accreditation_status: Mapped[str] = mapped_column(String(20), default="verified")  # pending, verified, expired
    accreditation_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user: Mapped["User"] = relationship("User", back_populates="investor_profile")


class Venture(Base):
    __tablename__ = "ventures"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("ven"))
    founder_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    cohort_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    thesis: Mapped[str] = mapped_column(Text, nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    clarity_score: Mapped[float] = mapped_column(Float, default=85.0)
    constraints: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)  # latency, compliance, squadSize...
    raised_cents: Mapped[int] = mapped_column(Integer, default=0)
    runway_months: Mapped[int] = mapped_column(Integer, default=12)
    mrr_cents: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    founder: Mapped["User"] = relationship("User", back_populates="ventures_founded")
    cohort: Mapped[Optional["Cohort"]] = relationship("Cohort", back_populates="ventures")
    squad_roles: Mapped[List["SquadRole"]] = relationship("SquadRole", back_populates="venture", cascade="all, delete-orphan")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="venture", cascade="all, delete-orphan")
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", back_populates="venture", cascade="all, delete-orphan")
    invitations: Mapped[List["Invitation"]] = relationship("Invitation", back_populates="venture", cascade="all, delete-orphan")
    cap_table_entries: Mapped[List["CapTableEntry"]] = relationship("CapTableEntry", back_populates="venture", cascade="all, delete-orphan")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="venture", cascade="all, delete-orphan")
    financial_snapshots: Mapped[List["FinancialSnapshot"]] = relationship("FinancialSnapshot", back_populates="venture", cascade="all, delete-orphan")
    funding_requests: Mapped[List["FundingRequest"]] = relationship("FundingRequest", back_populates="venture", cascade="all, delete-orphan")
    investments: Mapped[List["Investment"]] = relationship("Investment", back_populates="venture")
    milestone_updates: Mapped[List["MilestoneUpdate"]] = relationship("MilestoneUpdate", back_populates="venture", cascade="all, delete-orphan")


class SquadRole(Base):
    __tablename__ = "squad_roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("rol"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="vacant", index=True)  # filled, vacant, reserved
    filled_by_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    requirements: Mapped[List[str]] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    # Relationships
    venture: Mapped["Venture"] = relationship("Venture", back_populates="squad_roles")
    matches: Mapped[List["Match"]] = relationship("Match", back_populates="role", cascade="all, delete-orphan")
    invitations: Mapped[List["Invitation"]] = relationship("Invitation", back_populates="role", cascade="all, delete-orphan")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="role", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_matches_role_worker"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("mat"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    candidate_code: Mapped[str] = mapped_column(String(50), nullable=False)
    synergy_score: Mapped[float] = mapped_column(Float, default=0.0)
    fit_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="suggested", index=True)  # suggested, invited, declined

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="matches")
    role: Mapped["SquadRole"] = relationship("SquadRole", back_populates="matches")
    worker: Mapped["User"] = relationship("User")


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("chl"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    duration_hours: Mapped[int] = mapped_column(Integer, default=48)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)  # open, closed

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="challenges")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="challenge", cascade="all, delete-orphan")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("sub"))
    challenge_id: Mapped[str] = mapped_column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), index=True, nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    candidate_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="in_review", index=True)  # in_review, attested
    score: Mapped[float] = mapped_column(Float, default=0.0)
    p99_latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    tests_passed: Mapped[int] = mapped_column(Integer, default=0)
    tests_total: Mapped[int] = mapped_column(Integer, default=0)
    hash: Mapped[str] = mapped_column(String(66), nullable=False)
    replay_integrity: Mapped[float] = mapped_column(Float, default=0.0)
    failure_recovery: Mapped[float] = mapped_column(Float, default=0.0)
    concurrency_latency: Mapped[float] = mapped_column(Float, default=0.0)
    code_elegance: Mapped[float] = mapped_column(Float, default=0.0)
    reviewer_verdict: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    challenge: Mapped["Challenge"] = relationship("Challenge", back_populates="submissions")
    worker: Mapped["User"] = relationship("User")


class ProofReport(Base):
    __tablename__ = "proof_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("prf"))
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    submission_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True)
    sprint_name: Mapped[str] = mapped_column(String(100), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    cohort_rank: Mapped[int] = mapped_column(Integer, default=1)
    hash: Mapped[str] = mapped_column(String(66), nullable=False)
    tests_passed: Mapped[int] = mapped_column(Integer, default=0)
    tests_total: Mapped[int] = mapped_column(Integer, default=0)
    p99_latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    memory_leak_bytes: Mapped[int] = mapped_column(Integer, default=0)
    reviewer_verdict: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    worker: Mapped["User"] = relationship("User")


class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_invitations_role_worker"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("inv"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0)
    terms: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)  # pending, accepted, declined
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="invitations")
    role: Mapped["SquadRole"] = relationship("SquadRole", back_populates="invitations")
    worker: Mapped["User"] = relationship("User")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_applications_role_worker"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("app"))
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True, nullable=False)
    worker_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    blind_token: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="submitted", index=True)  # submitted, reviewed

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    role: Mapped["SquadRole"] = relationship("SquadRole", back_populates="applications")
    worker: Mapped["User"] = relationship("User")


class CapTableEntry(Base):
    __tablename__ = "cap_table_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("cap"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    holder_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    holder_label: Mapped[str] = mapped_column(String(100), nullable=False)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0)
    kind: Mapped[str] = mapped_column(String(30), nullable=False)  # founder, cofounder, reserve, option_pool, investor_safe
    vested_pct: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="cap_table_entries")
    holder_user: Mapped[Optional["User"]] = relationship("User")


class RestructuringEvent(Base):
    __tablename__ = "restructuring_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("rst"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    from_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    to_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    equity_delta_pct: Mapped[float] = mapped_column(Float, default=0.0)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    venture: Mapped["Venture"] = relationship("Venture")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("txn"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    occurred_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # infrastructure, revenue, payroll, legal, other
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)  # signed int
    proof_hash: Mapped[str] = mapped_column(String(66), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="transactions")


class FinancialSnapshot(Base):
    __tablename__ = "financial_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("snp"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    month: Mapped[str] = mapped_column(String(7), nullable=False)  # YYYY-MM
    burn_cents: Mapped[int] = mapped_column(Integer, default=0)
    revenue_cents: Mapped[int] = mapped_column(Integer, default=0)
    cash_cents: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="financial_snapshots")


class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("opp"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # syndicate, micro_vc, grant
    check_min_cents: Mapped[int] = mapped_column(Integer, default=0)
    check_max_cents: Mapped[int] = mapped_column(Integer, default=0)
    structure: Mapped[str] = mapped_column(String(100), nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list)
    timeline: Mapped[str] = mapped_column(String(50), nullable=False)
    base_fit_pct: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    requests: Mapped[List["FundingRequest"]] = relationship("FundingRequest", back_populates="opportunity", cascade="all, delete-orphan")


class FundingRequest(Base):
    __tablename__ = "funding_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("fnr"))
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    funding_opportunity_id: Mapped[str] = mapped_column(String(36), ForeignKey("funding_opportunities.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="funding_requests")
    opportunity: Mapped["FundingOpportunity"] = relationship("FundingOpportunity", back_populates="requests")


class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("invst"))
    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="RESTRICT"), index=True, nullable=False)
    instrument_type: Mapped[str] = mapped_column(String(20), nullable=False)  # safe, grant
    instrument_label: Mapped[str] = mapped_column(String(100), nullable=False)
    principal_cents: Mapped[int] = mapped_column(Integer, default=0)
    val_cap_cents: Mapped[int] = mapped_column(Integer, default=0)
    discount_pct: Mapped[float] = mapped_column(Float, default=0.0)
    equity_pct: Mapped[float] = mapped_column(Float, default=0.0)
    contract_addr: Mapped[str] = mapped_column(String(100), nullable=False)
    signed_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    investor: Mapped["User"] = relationship("User")
    venture: Mapped["Venture"] = relationship("Venture", back_populates="investments")


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
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    venture: Mapped["Venture"] = relationship("Venture", back_populates="milestone_updates")
    reads: Mapped[List["MilestoneRead"]] = relationship("MilestoneRead", back_populates="update", cascade="all, delete-orphan")


class MilestoneRead(Base):
    __tablename__ = "milestone_reads"

    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    update_id: Mapped[str] = mapped_column(String(36), ForeignKey("milestone_updates.id", ondelete="CASCADE"), primary_key=True)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    investor: Mapped["User"] = relationship("User")
    update: Mapped["MilestoneUpdate"] = relationship("MilestoneUpdate", back_populates="reads")


class DisclosureRequest(Base):
    __tablename__ = "disclosure_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("dsc"))
    investor_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    venture_id: Mapped[str] = mapped_column(String(36), ForeignKey("ventures.id", ondelete="CASCADE"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    investor: Mapped["User"] = relationship("User")
    venture: Mapped["Venture"] = relationship("Venture")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("notif"))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(50), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped["User"] = relationship("User")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: generate_id("aud"))
    actor_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    actor: Mapped[Optional["User"]] = relationship("User")
