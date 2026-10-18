import datetime
from typing import List, Optional, Any
from sqlalchemy import (
    String, Integer, Float, Boolean, JSON, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from database.base import Base, TimestampMixin, utcnow


class WorkerProfile(Base, TimestampMixin):
    __tablename__ = "worker_profiles"

    user_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    experience_level: Mapped[str] = mapped_column(
        String(32),
        default="mid"
    )  # junior, mid, senior, founding
    skills: Mapped[Any] = mapped_column(
        JSON,
        default=list
    )  # JSON list of strings
    portfolio_url: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True
    )
    github_url: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True
    )
    whatsapp_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    cloaked: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )  # Default True per SHARED_CONTRACT.md section 5 & 6
    weekly_availability_hours: Mapped[int] = mapped_column(
        Integer,
        default=20
    )
    percentile: Mapped[float] = mapped_column(
        Float,
        default=95.0
    )

    # String reference to Person A's User model
    user: Mapped["User"] = relationship(
        "User",
        backref=backref("worker_profile", uselist=False)
    )

    def __init__(self, **kwargs):
        kwargs.setdefault("cloaked", True)
        kwargs.setdefault("whatsapp_enabled", True)
        kwargs.setdefault("experience_level", "mid")
        kwargs.setdefault("weekly_availability_hours", 20)
        kwargs.setdefault("percentile", 95.0)
        if "skills" not in kwargs:
            kwargs["skills"] = []
        super().__init__(**kwargs)
