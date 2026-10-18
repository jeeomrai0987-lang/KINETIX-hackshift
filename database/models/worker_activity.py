import datetime
from typing import List, Optional, Any
from sqlalchemy import (
    String, Integer, Float, Boolean, Text, DateTime, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin, utcnow


class Submission(Base, TimestampMixin):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    challenge_id: Mapped[str] = mapped_column(String(64), ForeignKey("challenges.id", ondelete="CASCADE"), index=True)
    worker_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    candidate_code: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="in_review", index=True)  # in_review, attested
    score: Mapped[float] = mapped_column(Float, default=0.0)
    p99_latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    tests_passed: Mapped[int] = mapped_column(Integer, default=0)
    tests_total: Mapped[int] = mapped_column(Integer, default=0)
    hash: Mapped[str] = mapped_column(String(128))
    replay_integrity: Mapped[float] = mapped_column(Float, default=0.0)
    failure_recovery: Mapped[float] = mapped_column(Float, default=0.0)
    concurrency_latency: Mapped[float] = mapped_column(Float, default=0.0)
    code_elegance: Mapped[float] = mapped_column(Float, default=0.0)
    reviewer_verdict: Mapped[str] = mapped_column(String(255), default="")
    signed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    challenge: Mapped["Challenge"] = relationship("Challenge")
    worker: Mapped["User"] = relationship("User", foreign_keys=[worker_id])
    proof_report: Mapped[Optional["ProofReport"]] = relationship("ProofReport", back_populates="submission", uselist=False)


class ProofReport(Base, TimestampMixin):
    __tablename__ = "proof_reports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    worker_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    submission_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True, index=True)
    sprint_name: Mapped[str] = mapped_column(String(255))
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utcnow)
    score: Mapped[float] = mapped_column(Float)
    cohort_rank: Mapped[str] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(128))
    tests_passed: Mapped[int] = mapped_column(Integer)
    tests_total: Mapped[int] = mapped_column(Integer)
    p99_latency_ms: Mapped[float] = mapped_column(Float)
    memory_leak_bytes: Mapped[int] = mapped_column(Integer, default=0)
    reviewer_verdict: Mapped[str] = mapped_column(String(255))

    worker: Mapped["User"] = relationship("User", foreign_keys=[worker_id])
    submission: Mapped[Optional["Submission"]] = relationship("Submission", back_populates="proof_report")


class Invitation(Base, TimestampMixin):
    __tablename__ = "invitations"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_invitation_role_worker"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    venture_id: Mapped[str] = mapped_column(String(64), ForeignKey("ventures.id", ondelete="CASCADE"), index=True)
    role_id: Mapped[str] = mapped_column(String(64), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True)
    worker_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    equity_pct: Mapped[float] = mapped_column(Float)
    terms: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)  # pending, accepted, declined
    responded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    venture: Mapped["Venture"] = relationship("Venture")
    role: Mapped["SquadRole"] = relationship("SquadRole")
    worker: Mapped["User"] = relationship("User", foreign_keys=[worker_id])


class Application(Base, TimestampMixin):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("role_id", "worker_id", name="uq_application_role_worker"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    role_id: Mapped[str] = mapped_column(String(64), ForeignKey("squad_roles.id", ondelete="CASCADE"), index=True)
    worker_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    blind_token: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="submitted", index=True)  # submitted, reviewed

    role: Mapped["SquadRole"] = relationship("SquadRole")
    worker: Mapped["User"] = relationship("User", foreign_keys=[worker_id])
