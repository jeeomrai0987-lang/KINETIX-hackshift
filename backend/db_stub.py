"""
High-fidelity database stub and model definition for VentureForge AI.
Used by backend/app/db.py when the top-level database package has not yet been pushed by Person A/C.
Implements SQLAlchemy 2.0 models according to docs/SHARED_CONTRACT.md Sections 5, 6, and 7.
"""

from __future__ import annotations
import os
import json
import uuid
import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, Text, JSON,
    ForeignKey, DateTime, UniqueConstraint, Index, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import bcrypt

Base = declarative_base()

# --- Helper ID generator ---
def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

# --- Models (Section 5) ---

class Cohort(Base):
    __tablename__ = "cohorts"
    id = Column(String, primary_key=True, default=lambda: make_id("coh"))
    name = Column(String, nullable=False)
    batch_no = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    users = relationship("User", back_populates="cohort")
    ventures = relationship("Venture", back_populates="cohort")


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: make_id("usr"))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # founder, investor, worker
    title = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    node_id = Column(String, nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    cohort_id = Column(String, ForeignKey("cohorts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    cohort = relationship("Cohort", back_populates="users")
    worker_profile = relationship("WorkerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    investor_profile = relationship("InvestorProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    ventures = relationship("Venture", back_populates="founder")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class WorkerProfile(Base):
    __tablename__ = "worker_profiles"
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    experience_level = Column(String, default="mid")  # junior, mid, senior, founding
    skills = Column(JSON, default=list)
    portfolio_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    whatsapp_enabled = Column(Boolean, default=False)
    cloaked = Column(Boolean, default=True)
    weekly_availability_hours = Column(Integer, default=40)
    percentile = Column(Integer, default=96)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="worker_profile")


class InvestorProfile(Base):
    __tablename__ = "investor_profiles"
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tier = Column(String, default="Syndicate Tier 1")
    wallet_address = Column(String, nullable=True)
    preferred_sectors = Column(JSON, default=list)
    instant_alerts = Column(Boolean, default=True)
    weekly_digest = Column(Boolean, default=True)
    accreditation_status = Column(String, default="verified")  # pending, verified, expired
    accreditation_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="investor_profile")


class Venture(Base):
    __tablename__ = "ventures"
    id = Column(String, primary_key=True, default=lambda: make_id("ven"))
    founder_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    cohort_id = Column(String, ForeignKey("cohorts.id"), nullable=True)
    name = Column(String, nullable=False)
    thesis = Column(Text, nullable=False)
    sector = Column(String, nullable=False)
    stage = Column(String, default="Sprint 3 / Proof-of-Work")
    clarity_score = Column(Integer, default=94)
    constraints = Column(JSON, default=dict)
    raised_cents = Column(Integer, default=0)
    runway_months = Column(Integer, default=18)
    mrr_cents = Column(Integer, default=0)
    status = Column(String, default="active", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    founder = relationship("User", back_populates="ventures")
    cohort = relationship("Cohort", back_populates="ventures")
    squad_roles = relationship("SquadRole", back_populates="venture", cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="venture", cascade="all, delete-orphan")
    challenges = relationship("Challenge", back_populates="venture", cascade="all, delete-orphan")
    invitations = relationship("Invitation", back_populates="venture", cascade="all, delete-orphan")
    cap_table_entries = relationship("CapTableEntry", back_populates="venture", cascade="all, delete-orphan")
    restructuring_events = relationship("RestructuringEvent", back_populates="venture", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="venture", cascade="all, delete-orphan")
    financial_snapshots = relationship("FinancialSnapshot", back_populates="venture", cascade="all, delete-orphan")
    funding_requests = relationship("FundingRequest", back_populates="venture", cascade="all, delete-orphan")
    investments = relationship("Investment", back_populates="venture", cascade="all, delete-orphan")
    milestone_updates = relationship("MilestoneUpdate", back_populates="venture", cascade="all, delete-orphan")


class SquadRole(Base):
    __tablename__ = "squad_roles"
    id = Column(String, primary_key=True, default=lambda: make_id("rol"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    equity_pct = Column(Float, default=15.0)
    status = Column(String, default="vacant")  # filled, vacant, reserved
    filled_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    requirements = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    venture = relationship("Venture", back_populates="squad_roles")
    filled_by = relationship("User", foreign_keys=[filled_by_user_id])
    matches = relationship("Match", back_populates="role", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="role", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_matches_role_worker"),
    )
    id = Column(String, primary_key=True, default=lambda: make_id("mat"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(String, ForeignKey("squad_roles.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_code = Column(String, nullable=False)
    synergy_score = Column(Integer, default=95)
    fit_details = Column(JSON, default=dict)
    status = Column(String, default="suggested", index=True)  # suggested, invited, declined
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="matches")
    role = relationship("SquadRole", back_populates="matches")
    worker = relationship("User", foreign_keys=[worker_id])


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(String, primary_key=True, default=lambda: make_id("chg"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(String, ForeignKey("squad_roles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    duration_hours = Column(Integer, default=48)
    starts_at = Column(DateTime, default=datetime.datetime.utcnow)
    ends_at = Column(DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=48))
    status = Column(String, default="open", index=True)  # open, closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="challenges")
    submissions = relationship("Submission", back_populates="challenge", cascade="all, delete-orphan")


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(String, primary_key=True, default=lambda: make_id("sub"))
    challenge_id = Column(String, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    worker_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_code = Column(String, nullable=False)
    status = Column(String, default="in_review", index=True)  # in_review, attested
    score = Column(Integer, default=98)
    p99_latency_ms = Column(Float, default=1.84)
    tests_passed = Column(Integer, default=48)
    tests_total = Column(Integer, default=48)
    hash = Column(String, nullable=False)
    replay_integrity = Column(Float, default=99.8)
    failure_recovery = Column(Float, default=100.0)
    concurrency_latency = Column(Float, default=98.4)
    code_elegance = Column(Float, default=96.0)
    reviewer_verdict = Column(Text, default="Benchmark attestation passed with zero regression.")
    signed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="submissions")
    worker = relationship("User", foreign_keys=[worker_id])
    proof_reports = relationship("ProofReport", back_populates="submission")


class ProofReport(Base):
    __tablename__ = "proof_reports"
    id = Column(String, primary_key=True, default=lambda: make_id("rep"))
    worker_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_id = Column(String, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True)
    sprint_name = Column(String, nullable=False)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    score = Column(Integer, default=99)
    cohort_rank = Column(String, default="Top 1%")
    hash = Column(String, nullable=False)
    tests_passed = Column(Integer, default=48)
    tests_total = Column(Integer, default=48)
    p99_latency_ms = Column(Float, default=1.84)
    memory_leak_bytes = Column(Integer, default=0)
    reviewer_verdict = Column(Text, default="Cryptographically signed by automated test harness.")
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    submission = relationship("Submission", back_populates="proof_reports")
    worker = relationship("User", foreign_keys=[worker_id])


class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_invitations_role_worker"),
    )
    id = Column(String, primary_key=True, default=lambda: make_id("inv"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(String, ForeignKey("squad_roles.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    equity_pct = Column(Float, default=15.0)
    terms = Column(Text, nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending", index=True)  # pending, accepted, declined
    responded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="invitations")
    role = relationship("SquadRole")
    worker = relationship("User", foreign_keys=[worker_id])


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_applications_role_worker"),
    )
    id = Column(String, primary_key=True, default=lambda: make_id("app"))
    role_id = Column(String, ForeignKey("squad_roles.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    blind_token = Column(String, nullable=False)
    status = Column(String, default="submitted", index=True)  # submitted, reviewed
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    role = relationship("SquadRole", back_populates="applications")
    worker = relationship("User", foreign_keys=[worker_id])


class CapTableEntry(Base):
    __tablename__ = "cap_table_entries"
    id = Column(String, primary_key=True, default=lambda: make_id("cap"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    holder_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    holder_label = Column(String, nullable=False)
    equity_pct = Column(Float, nullable=False)
    kind = Column(String, nullable=False)  # founder, cofounder, reserve, option_pool, investor_safe
    vested_pct = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    venture = relationship("Venture", back_populates="cap_table_entries")
    holder = relationship("User", foreign_keys=[holder_user_id])


class RestructuringEvent(Base):
    __tablename__ = "restructuring_events"
    id = Column(String, primary_key=True, default=lambda: make_id("rst"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String, nullable=False)  # e.g. rebalance, succession, dilution
    from_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    to_user_id = Column(String, ForeignKey("users.id"), nullable=True)
    equity_delta_pct = Column(Float, nullable=False)
    stage = Column(String, default="Draft")
    note = Column(Text, nullable=True)
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="restructuring_events")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=lambda: make_id("tx"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    occurred_on = Column(String, nullable=False)  # YYYY-MM-DD
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)  # infrastructure, revenue, payroll, legal, other
    amount_cents = Column(Integer, nullable=False)  # signed cents
    proof_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="transactions")


class FinancialSnapshot(Base):
    __tablename__ = "financial_snapshots"
    id = Column(String, primary_key=True, default=lambda: make_id("snp"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    month = Column(String, nullable=False)  # YYYY-MM
    burn_cents = Column(Integer, nullable=False)
    revenue_cents = Column(Integer, nullable=False)
    cash_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="financial_snapshots")


class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"
    id = Column(String, primary_key=True, default=lambda: make_id("fnd"))
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # syndicate, micro_vc, grant
    check_min_cents = Column(Integer, default=5000000)
    check_max_cents = Column(Integer, default=25000000)
    structure = Column(String, default="Post-money SAFE")
    tags = Column(JSON, default=list)
    timeline = Column(String, default="2-3 weeks")
    base_fit_pct = Column(Float, default=92.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    requests = relationship("FundingRequest", back_populates="opportunity", cascade="all, delete-orphan")


class FundingRequest(Base):
    __tablename__ = "funding_requests"
    id = Column(String, primary_key=True, default=lambda: make_id("frq"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    funding_opportunity_id = Column(String, ForeignKey("funding_opportunities.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="requested", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="funding_requests")
    opportunity = relationship("FundingOpportunity", back_populates="requests")


class Investment(Base):
    __tablename__ = "investments"
    id = Column(String, primary_key=True, default=lambda: make_id("invst"))
    investor_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    instrument_type = Column(String, default="safe")  # safe, grant
    instrument_label = Column(String, default="Post-Money SAFE (YC Standard)")
    principal_cents = Column(Integer, nullable=False)
    val_cap_cents = Column(Integer, nullable=False)
    discount_pct = Column(Float, default=20.0)
    equity_pct = Column(Float, default=5.0)
    contract_addr = Column(String, default="0x71c...39b")
    signed_on = Column(String, nullable=False)
    status = Column(String, default="active", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    investor = relationship("User", foreign_keys=[investor_id])
    venture = relationship("Venture", back_populates="investments")


class MilestoneUpdate(Base):
    __tablename__ = "milestone_updates"
    id = Column(String, primary_key=True, default=lambda: make_id("mls"))
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    headline = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    stage_label = Column(String, default="Sprint 3 Attestation")
    tag = Column(String, default="Engineering")
    merkle_proof = Column(String, nullable=False)
    deliverables = Column(JSON, default=list)
    metrics = Column(JSON, default=dict)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    venture = relationship("Venture", back_populates="milestone_updates")
    reads = relationship("MilestoneRead", back_populates="update", cascade="all, delete-orphan")


class MilestoneRead(Base):
    __tablename__ = "milestone_reads"
    investor_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    update_id = Column(String, ForeignKey("milestone_updates.id", ondelete="CASCADE"), primary_key=True)
    read_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    update = relationship("MilestoneUpdate", back_populates="reads")


class DisclosureRequest(Base):
    __tablename__ = "disclosure_requests"
    id = Column(String, primary_key=True, default=lambda: make_id("dsc"))
    investor_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    venture_id = Column(String, ForeignKey("ventures.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, default="pending", index=True)  # pending, approved, declined
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    investor = relationship("User", foreign_keys=[investor_id])
    venture = relationship("Venture")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: make_id("notif"))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    kind = Column(String, default="system")
    body = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(String, primary_key=True, default=lambda: make_id("aud"))
    actor_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


# Container to mimic `models.*`
class ModelsContainer:
    Cohort = Cohort
    User = User
    WorkerProfile = WorkerProfile
    InvestorProfile = InvestorProfile
    Venture = Venture
    SquadRole = SquadRole
    Match = Match
    Challenge = Challenge
    Submission = Submission
    ProofReport = ProofReport
    Invitation = Invitation
    Application = Application
    CapTableEntry = CapTableEntry
    RestructuringEvent = RestructuringEvent
    Transaction = Transaction
    FinancialSnapshot = FinancialSnapshot
    FundingOpportunity = FundingOpportunity
    FundingRequest = FundingRequest
    Investment = Investment
    MilestoneUpdate = MilestoneUpdate
    MilestoneRead = MilestoneRead
    DisclosureRequest = DisclosureRequest
    Notification = Notification
    AuditLog = AuditLog

models = ModelsContainer()


# --- Database Session Setup ---

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./ventureforge.db")
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Demo Cast Seeder (Section 7) ---

def hash_pw(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def seed_demo_data(db: Session):
    # Only seed if no cohort or users exist
    if db.query(User).first() is not None:
        return

    default_pw_hash = hash_pw("Demo#2026")

    # Cohort
    cohort = Cohort(
        id="coh_alpha_25",
        name="Cohort Alpha",
        batch_no="Alpha Batch '25"
    )
    db.add(cohort)

    # Cast from Section 7
    # 1. usr_founder_01: Alex Mercer
    u_founder = User(
        id="usr_founder_01",
        name="Alex Mercer",
        email="alex.mercer@synthetix.ai",
        password_hash=default_pw_hash,
        role="founder",
        title="CEO / Founder",
        avatar_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCrFd9FXpH1DVp90x6QYI3kcBlABNYtgFYxaa-elUwjSWxyV56HX1Uir3Bo-JqKk3TkfehwV64tbjsMvhw9FVCYgdY2H_bGj_WUycEQb8Dik8Hw6UG-DAyLKzDMeTucfRCt_DgSFD6L_pCOl0A8YFS_ujCydDFtmuuoeY7hOIu_gb7QgAuFUQWPIUNLCYl78krYPxXqb-rVILLe9UGsKUdf2HDshK8T-ZrUTNmAMRphT1t5VEKD26jNtQ",
        node_id="NODE-FND-0001",
        verified=True,
        cohort_id=cohort.id,
    )

    # 2. usr_worker_03: Elena Vance
    u_worker_03 = User(
        id="usr_worker_03",
        name="Elena Vance",
        email="elena.vance@startup.io",
        password_hash=default_pw_hash,
        role="worker",
        title="Distributed Systems Architect",
        avatar_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAXDAn8ZFbqaXgUtAZFPSAMimDjdAoYUtHj9L77g4tSh_dzBGXy6q7ARHBvvPaEiQBevjgoVWtUl1CPRgJcoZ_Gyr1x8Zo7gNTBlUQObPUZdavCilarTN6yVjeMbRs58962jPDHojUKOmZ_bPn3g6RPFzhAkTcS32gCbsLDrLoGoPt23xW2bo98EiFz6_G89_dt-TciA5PCjPGcobNbxFBrua1O80BXj8xC1JSaqoZGvJJLCVcC2Qyt0g",
        node_id="TX-5512B",
        verified=True,
        cohort_id=cohort.id,
    )
    p_worker_03 = WorkerProfile(
        user_id="usr_worker_03",
        experience_level="senior",
        skills=["Distributed Systems", "Rust", "Go", "System Architecture"],
        portfolio_url="https://github.com/elena-vance",
        github_url="https://github.com/elena-vance",
        phone="+1 (555) 019-2831",
        whatsapp_enabled=True,
        cloaked=True,
        weekly_availability_hours=40,
        percentile=98
    )

    # 3. usr_investor_02: Marcus Vance
    u_investor_02 = User(
        id="usr_investor_02",
        name="Marcus Vance",
        email="marcus.vance@angelsyndicate.vc",
        password_hash=default_pw_hash,
        role="investor",
        title="General Partner",
        avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80",
        node_id="NODE-INV-8841Z",
        verified=True,
        cohort_id=cohort.id,
    )
    p_investor_02 = InvestorProfile(
        user_id="usr_investor_02",
        tier="Syndicate Tier 1",
        wallet_address="0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
        preferred_sectors=["Autonomous Agents", "Enterprise Infrastructure", "DevTools"],
        instant_alerts=True,
        weekly_digest=True,
        accreditation_status="verified",
        accreditation_expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)
    )

    # 4. usr_worker_04: Julian Vance
    u_worker_04 = User(
        id="usr_worker_04",
        name="Julian Vance",
        email="julian.vance@talenthub.ai",
        password_hash=default_pw_hash,
        role="worker",
        title="ML Infrastructure Lead",
        node_id="TX-9042A",
        verified=True,
        cohort_id=cohort.id,
    )
    p_worker_04 = WorkerProfile(
        user_id="usr_worker_04",
        experience_level="senior",
        skills=["PyTorch", "CUDA", "C++", "Kernel Optimization"],
        cloaked=True,
        percentile=99
    )

    # 5. usr_worker_05: Elena Rostova
    u_worker_05 = User(
        id="usr_worker_05",
        name="Elena Rostova",
        email="elena.rostova@kernelops.io",
        password_hash=default_pw_hash,
        role="worker",
        title="Security & Systems Engineer",
        node_id="TX-8821B",
        verified=True,
        cohort_id=cohort.id,
    )
    p_worker_05 = WorkerProfile(
        user_id="usr_worker_05",
        experience_level="mid",
        skills=["Rust", "eBPF", "Kubernetes", "Zero Trust"],
        cloaked=True,
        percentile=94
    )

    # 6. usr_cofounder_01: Marcus Chen
    u_cofounder_01 = User(
        id="usr_cofounder_01",
        name="Marcus Chen",
        email="marcus.chen@synthetix.ai",
        password_hash=default_pw_hash,
        role="founder",
        title="Co-Founder & CTO",
        node_id="NODE-FND-0002",
        verified=True,
        cohort_id=cohort.id,
    )

    # 7. usr_cofounder_02: Sarah Jenkins
    u_cofounder_02 = User(
        id="usr_cofounder_02",
        name="Sarah Jenkins",
        email="sarah.jenkins@synthetix.ai",
        password_hash=default_pw_hash,
        role="founder",
        title="Head of Enterprise Growth",
        node_id="NODE-FND-0003",
        verified=True,
        cohort_id=cohort.id,
    )

    db.add_all([
        u_founder, u_worker_03, p_worker_03, u_investor_02, p_investor_02,
        u_worker_04, p_worker_04, u_worker_05, p_worker_05,
        u_cofounder_01, u_cofounder_02
    ])
    db.flush()

    # Venture: Synthetix AI
    ven_synthetix = Venture(
        id="ven_synthetix",
        founder_id=u_founder.id,
        cohort_id=cohort.id,
        name="Synthetix AI",
        thesis="Autonomous distributed agent mesh operating with deterministic cryptographic consensus for mission-critical enterprise workflows.",
        sector="Autonomous Systems",
        stage="Sprint 3 / Proof-of-Work",
        clarity_score=94,
        constraints={
            "latency": "< 2.0ms p99",
            "compliance": "SOC2 / FedRAMP ready",
            "squadSize": "4 core nodes",
            "compute": "H100 NVLink Cluster"
        },
        raised_cents=125000000,   # $1.25M
        runway_months=18,
        mrr_cents=4200000,        # $42k MRR
        status="active"
    )

    # Extra ventures from Section 7
    ven_polymatrix = Venture(
        id="ven_polymatrix",
        founder_id=u_founder.id,
        cohort_id=cohort.id,
        name="PolyMatrix AI",
        thesis="Zero-knowledge verifiable compute network for multi-modal frontier models.",
        sector="ZK Compute",
        stage="Seed / Accelerated",
        clarity_score=91,
        raised_cents=200000000,
        runway_months=22,
        mrr_cents=2800000,
        status="active"
    )
    ven_chronodb = Venture(
        id="ven_chronodb",
        founder_id=u_founder.id,
        cohort_id=cohort.id,
        name="ChronoDB",
        thesis="Time-series ledger optimized for high-frequency robotic telemetry streams.",
        sector="Data Infrastructure",
        stage="Incubation",
        clarity_score=88,
        raised_cents=50000000,
        runway_months=14,
        mrr_cents=1200000,
        status="active"
    )
    ven_aether = Venture(
        id="ven_aether",
        founder_id=u_founder.id,
        cohort_id=cohort.id,
        name="Aether Labs",
        thesis="Decentralized simulation sandbox for embodied robotics and spatial AI.",
        sector="Spatial Computing",
        stage="Pre-Seed",
        clarity_score=86,
        raised_cents=75000000,
        runway_months=16,
        mrr_cents=800000,
        status="active"
    )
    ven_kauri = Venture(
        id="ven_kauri",
        founder_id=u_founder.id,
        cohort_id=cohort.id,
        name="Kauri Health",
        thesis="Federated clinical AI pipeline preserving HIPAA compliance across hospital consortia.",
        sector="Healthcare AI",
        stage="Seed",
        clarity_score=93,
        raised_cents=150000000,
        runway_months=20,
        mrr_cents=3500000,
        status="active"
    )

    db.add_all([ven_synthetix, ven_polymatrix, ven_chronodb, ven_aether, ven_kauri])
    db.flush()

    # Squad Roles for Synthetix
    r1 = SquadRole(
        id="rol_cto",
        venture_id=ven_synthetix.id,
        title="Co-Founder & CTO",
        description="Architecture of distributed consensus engine and verifiable state machine.",
        equity_pct=25.0,
        status="filled",
        filled_by_user_id=u_cofounder_01.id,
        requirements=["Distributed Systems", "Rust", "Consensus Algorithms"]
    )
    r2 = SquadRole(
        id="rol_growth",
        venture_id=ven_synthetix.id,
        title="Head of Enterprise Growth",
        description="Enterprise sales, SOC2 compliance partnerships, and pilot expansion.",
        equity_pct=15.0,
        status="filled",
        filled_by_user_id=u_cofounder_02.id,
        requirements=["Enterprise GTM", "B2B SaaS", "Security Compliance"]
    )
    r3 = SquadRole(
        id="rol_dist_sys",
        venture_id=ven_synthetix.id,
        title="Founding Distributed Systems Engineer",
        description="Low-latency p99 memory-safe networking layer and Raft cluster orchestration.",
        equity_pct=15.0,
        status="vacant",
        requirements=["Distributed Systems", "Rust", "Go", "p99 Latency Optimization"]
    )
    r4 = SquadRole(
        id="rol_ml_eng",
        venture_id=ven_synthetix.id,
        title="Lead Inference Systems Engineer",
        description="vLLM kernels, speculative decoding, and tensor parallel throughput.",
        equity_pct=10.0,
        status="vacant",
        requirements=["CUDA", "PyTorch", "vLLM", "C++"]
    )
    db.add_all([r1, r2, r3, r4])
    db.flush()

    # Cap Table Entries (sum to 100.0)
    # Alex Mercer: 40.0%
    # Marcus Chen: 25.0%
    # Sarah Jenkins: 15.0%
    # Option Pool (Reserved): 10.0%
    # Syndicate SAFE: 10.0%
    # Total = 100.0%
    cap_entries = [
        CapTableEntry(
            id="cap_01",
            venture_id=ven_synthetix.id,
            holder_user_id=u_founder.id,
            holder_label="Alex Mercer (CEO)",
            equity_pct=40.0,
            kind="founder",
            vested_pct=100.0
        ),
        CapTableEntry(
            id="cap_02",
            venture_id=ven_synthetix.id,
            holder_user_id=u_cofounder_01.id,
            holder_label="Marcus Chen (CTO)",
            equity_pct=25.0,
            kind="cofounder",
            vested_pct=75.0
        ),
        CapTableEntry(
            id="cap_03",
            venture_id=ven_synthetix.id,
            holder_user_id=u_cofounder_02.id,
            holder_label="Sarah Jenkins (Growth)",
            equity_pct=15.0,
            kind="cofounder",
            vested_pct=50.0
        ),
        CapTableEntry(
            id="cap_04",
            venture_id=ven_synthetix.id,
            holder_user_id=None,
            holder_label="Unallocated ESOP Pool",
            equity_pct=10.0,
            kind="option_pool",
            vested_pct=0.0
        ),
        CapTableEntry(
            id="cap_05",
            venture_id=ven_synthetix.id,
            holder_user_id=u_investor_02.id,
            holder_label="Marcus Vance (Angel Syndicate)",
            equity_pct=10.0,
            kind="investor_safe",
            vested_pct=100.0
        ),
    ]
    db.add_all(cap_entries)

    # Matches
    m1 = Match(
        id="mat_01",
        venture_id=ven_synthetix.id,
        role_id=r3.id,
        worker_id=u_worker_03.id,
        candidate_code="TX-5512B",
        synergy_score=97,
        fit_details={"technicalMatch": 98, "experienceMatch": 95, "availabilityMatch": 100},
        status="suggested"
    )
    m2 = Match(
        id="mat_02",
        venture_id=ven_synthetix.id,
        role_id=r4.id,
        worker_id=u_worker_04.id,
        candidate_code="TX-9042A",
        synergy_score=94,
        fit_details={"technicalMatch": 96, "experienceMatch": 92, "availabilityMatch": 95},
        status="suggested"
    )
    m3 = Match(
        id="mat_03",
        venture_id=ven_synthetix.id,
        role_id=r3.id,
        worker_id=u_worker_05.id,
        candidate_code="TX-8821B",
        synergy_score=91,
        fit_details={"technicalMatch": 90, "experienceMatch": 92, "availabilityMatch": 90},
        status="suggested"
    )
    db.add_all([m1, m2, m3])

    # Challenge
    chg = Challenge(
        id="chg_synthetix_01",
        venture_id=ven_synthetix.id,
        role_id=r3.id,
        title="48-Hour Low Latency Consensus Sprint",
        duration_hours=48,
        starts_at=datetime.datetime.utcnow() - datetime.timedelta(hours=24),
        ends_at=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        status="open"
    )
    db.add(chg)
    db.flush()

    # Submission
    sub = Submission(
        id="sub_elena_01",
        challenge_id=chg.id,
        worker_id=u_worker_03.id,
        candidate_code="TX-5512B",
        status="attested",
        score=99,
        p99_latency_ms=1.84,
        tests_passed=48,
        tests_total=48,
        hash="0x4b7f892a01c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4",
        replay_integrity=99.8,
        failure_recovery=100.0,
        concurrency_latency=98.4,
        code_elegance=96.0,
        reviewer_verdict="Zero memory leaks detected. p99 latency 1.84ms meets all mission-critical criteria.",
        signed_at=datetime.datetime.utcnow()
    )
    db.add(sub)
    db.flush()

    # Proof Report
    rep = ProofReport(
        id="rep_elena_01",
        worker_id=u_worker_03.id,
        submission_id=sub.id,
        sprint_name="Sprint 3 / Distributed Consensus",
        completed_at=datetime.datetime.utcnow(),
        score=99,
        cohort_rank="Top 1%",
        hash="0x4b7f892a01c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4",
        tests_passed=48,
        tests_total=48,
        p99_latency_ms=1.84,
        memory_leak_bytes=0,
        reviewer_verdict="Signed by automated zero-bias test harness on Arbitrum simulated L2 root."
    )
    db.add(rep)

    # Invitation
    inv = Invitation(
        id="inv_01",
        venture_id=ven_synthetix.id,
        role_id=r3.id,
        worker_id=u_worker_03.id,
        equity_pct=15.0,
        terms="4-year vesting with 1-year cliff. Co-founder equity allocation upon acceptance.",
        message="Your sprint submission exceeded our latency and robustness thresholds. We would be thrilled to have you join our core squad.",
        status="pending"
    )
    db.add(inv)

    # Transactions (6 entries)
    txs = [
        Transaction(
            id="tx_01",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-28",
            description="Enterprise Pilot Contract — Global FinTech Corp",
            category="revenue",
            amount_cents=4500000,
            proof_hash="0x9a8b7c6d5e4f3a2b1c0d"
        ),
        Transaction(
            id="tx_02",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-24",
            description="AWS & LambdaLabs GPU Cluster Compute Reservation",
            category="infrastructure",
            amount_cents=-1820000,
            proof_hash="0x1a2b3c4d5e6f7a8b9c0d"
        ),
        Transaction(
            id="tx_03",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-20",
            description="Core Engineering Sprint Compensation",
            category="payroll",
            amount_cents=-2400000,
            proof_hash="0x2b3c4d5e6f7a8b9c0d1e"
        ),
        Transaction(
            id="tx_04",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-15",
            description="SOC2 Type II Audit & FedRAMP Readiness",
            category="legal",
            amount_cents=-750000,
            proof_hash="0x3c4d5e6f7a8b9c0d1e2f"
        ),
        Transaction(
            id="tx_05",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-10",
            description="Cooley LLP Delaware C-Corp IP Assignment",
            category="legal",
            amount_cents=-450000,
            proof_hash="0x4d5e6f7a8b9c0d1e2f3a"
        ),
        Transaction(
            id="tx_06",
            venture_id=ven_synthetix.id,
            occurred_on="2026-03-01",
            description="Angel Syndicate Pre-Seed SAFE Tranche 1",
            category="revenue",
            amount_cents=50000000,
            proof_hash="0x5e6f7a8b9c0d1e2f3a4b"
        ),
    ]
    db.add_all(txs)

    # 6 months of Financial Snapshots
    snapshots = [
        FinancialSnapshot(id="snp_01", venture_id=ven_synthetix.id, month="2025-10", burn_cents=3200000, revenue_cents=1200000, cash_cents=145000000),
        FinancialSnapshot(id="snp_02", venture_id=ven_synthetix.id, month="2025-11", burn_cents=3400000, revenue_cents=1800000, cash_cents=143400000),
        FinancialSnapshot(id="snp_03", venture_id=ven_synthetix.id, month="2025-12", burn_cents=3800000, revenue_cents=2500000, cash_cents=142100000),
        FinancialSnapshot(id="snp_04", venture_id=ven_synthetix.id, month="2026-01", burn_cents=4100000, revenue_cents=3100000, cash_cents=141100000),
        FinancialSnapshot(id="snp_05", venture_id=ven_synthetix.id, month="2026-02", burn_cents=4400000, revenue_cents=3800000, cash_cents=140500000),
        FinancialSnapshot(id="snp_06", venture_id=ven_synthetix.id, month="2026-03", burn_cents=4500000, revenue_cents=4200000, cash_cents=140200000),
    ]
    db.add_all(snapshots)

    # Funding Opportunities
    f_opps = [
        FundingOpportunity(
            id="fnd_01",
            name="Apex Agentic Syndicate",
            category="syndicate",
            check_min_cents=10000000,
            check_max_cents=50000000,
            structure="Post-money SAFE (YC standard)",
            tags=["AI Agents", "Autonomous Consensus", "Fast-Track"],
            timeline="10-14 days",
            base_fit_pct=96.0
        ),
        FundingOpportunity(
            id="fnd_02",
            name="Frontier Horizon Micro-VC",
            category="micro_vc",
            check_min_cents=25000000,
            check_max_cents=100000000,
            structure="Priced Seed Equity",
            tags=["Enterprise Infrastructure", "DeepTech", "Lead Check"],
            timeline="3-4 weeks",
            base_fit_pct=92.0
        ),
        FundingOpportunity(
            id="fnd_03",
            name="NSF SBIR Phase I AI Grant",
            category="grant",
            check_min_cents=27500000,
            check_max_cents=27500000,
            structure="Non-dilutive Government Grant",
            tags=["Non-Dilutive", "Verifiable AI", "Research"],
            timeline="60 days",
            base_fit_pct=88.0
        ),
    ]
    db.add_all(f_opps)

    # Investment for Marcus Vance
    invst = Investment(
        id="invst_01",
        investor_id=u_investor_02.id,
        venture_id=ven_synthetix.id,
        instrument_type="safe",
        instrument_label="Post-Money SAFE ($10M Cap)",
        principal_cents=50000000,   # $500k
        val_cap_cents=1000000000,  # $10M Cap
        discount_pct=20.0,
        equity_pct=5.0,
        contract_addr="0x71c563e41c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a",
        signed_on="2026-02-15",
        status="active"
    )
    db.add(invst)

    # Milestone Update
    m_update = MilestoneUpdate(
        id="mls_01",
        venture_id=ven_synthetix.id,
        headline="Sprint 3 Verifiable Consensus Engine Attested at 1.84ms p99",
        body="Completed 48-hour soak test across 16 geo-distributed nodes. Zero packet loss, 100% Byzantine fault recovery, and deterministic cryptographic state hash logged to Arbitrum simulated testnet.",
        stage_label="Sprint 3 Attestation",
        tag="Engineering Milestone",
        merkle_proof="0x3f8a9b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9",
        deliverables=["48/48 integration tests passing", "p99 latency 1.84ms", "Zero memory leaks in 72h soak"],
        metrics={"p99LatencyMs": 1.84, "testsPassed": 48, "throughputRps": 24500},
        published_at=datetime.datetime.utcnow()
    )
    db.add(m_update)

    # Restructuring event demo
    rst = RestructuringEvent(
        id="rst_01",
        venture_id=ven_synthetix.id,
        type="Reserve Pool Rebalance",
        from_user_id=u_founder.id,
        to_user_id=None,
        equity_delta_pct=2.5,
        stage="Draft",
        note="Reallocating 2.5% from Founder allocation into ESOP Option Pool for upcoming founding engineer hires."
    )
    db.add(rst)

    # Audit log entry
    audit = AuditLog(
        id="aud_init_01",
        actor_id="system",
        action="seed_init",
        entity="venture",
        entity_id=ven_synthetix.id,
        payload={"note": "Initial demo seed loaded matching SHARED_CONTRACT.md"}
    )
    db.add(audit)

    db.commit()


# Automatically initialize tables and seed data if using stub
Base.metadata.create_all(bind=engine)
with SessionLocal() as db_session:
    seed_demo_data(db_session)
