"""Founder query helpers for VentureForge AI database layer.

These functions provide typed, high-performance query helpers for founder-facing
operations while respecting the contract rules (e.g., blind candidate protocol,
cap table 100.0% integrity check, and audit logging).
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session, joinedload

from database.models.core import User, AuditLog, Notification
from database.models.venture import Venture, SquadRole, Challenge, Match
from database.models.finance import (
    CapTableEntry,
    RestructuringEvent,
    Transaction,
    FinancialSnapshot,
    FundingOpportunity,
    FundingRequest,
)
from database.seed.common import canonical_hash, utcnow


def get_ventures_by_founder(db: Session, founder_id: str) -> List[Venture]:
    """Retrieve all ventures owned by a given founder."""
    stmt = (
        select(Venture)
        .where(Venture.founder_id == founder_id)
        .order_by(Venture.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def get_venture_by_id(db: Session, venture_id: str) -> Optional[Venture]:
    """Retrieve a single venture by ID."""
    stmt = select(Venture).where(Venture.id == venture_id)
    return db.scalars(stmt).first()


def get_founder_dashboard_summary(db: Session, venture_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve an aggregated summary for the founder dashboard.
    
    Includes venture basic metrics, squad count, average match synergy score,
    latest financial snapshot, and active challenge status.
    """
    venture = get_venture_by_id(db, venture_id)
    if not venture:
        return None

    # Squad roles summary
    roles_stmt = select(SquadRole).where(SquadRole.venture_id == venture_id)
    roles = list(db.scalars(roles_stmt).all())
    total_roles = len(roles)
    filled_roles = sum(1 for r in roles if r.status == "filled")
    vacant_roles = sum(1 for r in roles if r.status == "vacant")

    # Squad average synergy from matches
    matches_stmt = select(func.avg(Match.synergy_score)).where(
        Match.venture_id == venture_id
    )
    avg_synergy = db.scalar(matches_stmt) or 0.0

    # Latest financial snapshot
    latest_snapshot_stmt = (
        select(FinancialSnapshot)
        .where(FinancialSnapshot.venture_id == venture_id)
        .order_by(FinancialSnapshot.month.desc())
        .limit(1)
    )
    latest_snapshot = db.scalars(latest_snapshot_stmt).first()

    # Active challenge
    challenge_stmt = (
        select(Challenge)
        .where(Challenge.venture_id == venture_id, Challenge.status == "open")
        .limit(1)
    )
    active_challenge = db.scalars(challenge_stmt).first()

    return {
        "venture": venture,
        "squad": {
            "total_roles": total_roles,
            "filled_roles": filled_roles,
            "vacant_roles": vacant_roles,
            "avg_synergy_score": round(float(avg_synergy), 2),
        },
        "financials": {
            "raised_cents": venture.raised_cents,
            "runway_months": venture.runway_months,
            "mrr_cents": venture.mrr_cents,
            "latest_cash_cents": latest_snapshot.cash_cents if latest_snapshot else 0,
            "latest_burn_cents": latest_snapshot.burn_cents if latest_snapshot else 0,
        },
        "active_challenge": active_challenge,
    }


def get_squad_roles(db: Session, venture_id: str) -> List[SquadRole]:
    """List all squad roles for a venture with optional filled user details."""
    stmt = (
        select(SquadRole)
        .where(SquadRole.venture_id == venture_id)
        .order_by(SquadRole.created_at.asc())
    )
    return list(db.scalars(stmt).all())


def get_blind_matches_for_venture(db: Session, venture_id: str) -> List[Dict[str, Any]]:
    """Retrieve candidate matches for a venture respecting the Blind Protocol.
    
    Guarantees no worker personal identifying info (name, email, avatar, phone)
    is leaked. Only candidate_code, synergy_score, status, and fit_details are returned.
    """
    stmt = (
        select(Match, SquadRole.title)
        .join(SquadRole, Match.role_id == SquadRole.id)
        .where(Match.venture_id == venture_id)
        .order_by(Match.synergy_score.desc())
    )
    results = db.execute(stmt).all()
    
    sanitized = []
    for match, role_title in results:
        sanitized.append({
            "id": match.id,
            "venture_id": match.venture_id,
            "role_id": match.role_id,
            "role_title": role_title,
            "candidate_code": match.candidate_code,
            "synergy_score": match.synergy_score,
            "fit_details": match.fit_details,
            "status": match.status,
            "created_at": match.created_at,
        })
    return sanitized


# Alias per Contract Part A3 prompt
get_candidate_matches = get_blind_matches_for_venture


def get_cap_table(db: Session, venture_id: str) -> Tuple[List[CapTableEntry], float]:
    """Retrieve cap table entries and calculate total equity percentage.
    
    Returns (entries, total_equity_pct).
    """
    stmt = (
        select(CapTableEntry)
        .where(CapTableEntry.venture_id == venture_id)
        .order_by(CapTableEntry.equity_pct.desc())
    )
    entries = list(db.scalars(stmt).all())
    total_pct = sum(entry.equity_pct for entry in entries)
    return entries, round(total_pct, 4)


def validate_cap_table_integrity(db: Session, venture_id: str, tolerance: float = 0.001) -> bool:
    """Validate Contract Section 6 Rule 3:
    
    sum(equity_pct) over cap_table_entries must equal exactly 100.0% (+/- tolerance).
    """
    _, total_pct = get_cap_table(db, venture_id)
    return math.isclose(total_pct, 100.0, abs_tol=tolerance)


def get_financial_history(
    db: Session, venture_id: str, limit_months: int = 6
) -> List[FinancialSnapshot]:
    """Retrieve financial snapshots for a venture ordered chronologically."""
    stmt = (
        select(FinancialSnapshot)
        .where(FinancialSnapshot.venture_id == venture_id)
        .order_by(FinancialSnapshot.month.asc())
        .limit(limit_months)
    )
    return list(db.scalars(stmt).all())


def get_transactions(
    db: Session, venture_id: str, limit: int = 50, category: Optional[str] = None
) -> List[Transaction]:
    """Retrieve recent ledger transactions for a venture."""
    conditions = [Transaction.venture_id == venture_id]
    if category:
        conditions.append(Transaction.category == category)

    stmt = (
        select(Transaction)
        .where(and_(*conditions))
        .order_by(Transaction.occurred_on.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get_venture_financials(
    db: Session, venture_id: str, limit_months: int = 6
) -> Dict[str, Any]:
    """Retrieve comprehensive financial summary for a venture (Contract Part A3).
    
    Returns runway metrics, historical monthly snapshots, recent transactions,
    and cap table integrity status.
    """
    venture = get_venture_by_id(db, venture_id)
    snapshots = get_financial_history(db, venture_id, limit_months=limit_months)
    transactions = get_transactions(db, venture_id, limit=20)
    cap_entries, total_equity = get_cap_table(db, venture_id)

    return {
        "venture_id": venture_id,
        "raised_cents": venture.raised_cents if venture else 0,
        "runway_months": venture.runway_months if venture else 0,
        "mrr_cents": venture.mrr_cents if venture else 0,
        "snapshots": snapshots,
        "transactions": transactions,
        "cap_table": {
            "entries": cap_entries,
            "total_equity_pct": total_equity,
            "is_valid": math.isclose(total_equity, 100.0, abs_tol=0.001),
        },
    }


def get_funding_opportunities(
    db: Session, category: Optional[str] = None
) -> List[FundingOpportunity]:
    """List available funding opportunities, optionally filtered by category."""
    stmt = select(FundingOpportunity)
    if category:
        stmt = stmt.where(FundingOpportunity.category == category)
    stmt = stmt.order_by(FundingOpportunity.base_fit_pct.desc())
    return list(db.scalars(stmt).all())


def get_funding_requests(db: Session, venture_id: str) -> List[FundingRequest]:
    """List all funding requests submitted by a venture."""
    stmt = (
        select(FundingRequest)
        .where(FundingRequest.venture_id == venture_id)
        .order_by(FundingRequest.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def get_restructuring_events(db: Session, venture_id: str) -> List[RestructuringEvent]:
    """List all equity restructuring events for a venture."""
    stmt = (
        select(RestructuringEvent)
        .where(RestructuringEvent.venture_id == venture_id)
        .order_by(RestructuringEvent.created_at.desc())
    )
    return list(db.scalars(stmt).all())


def execute_equity_transfer(
    db: Session,
    venture_id: str,
    from_entry_id: str,
    to_entry_id: str,
    equity_pct: float,
    actor_id: str,
    stage: str = "execution",
    note: Optional[str] = None,
) -> RestructuringEvent:
    """Execute an atomic equity transfer between cap table entries.
    
    Guarantees:
    - Atomically updates equity_pct on both source and destination entries.
    - Ensures source entry has sufficient equity to transfer.
    - Verifies that cap table sum remains exactly 100.0%.
    - Records RestructuringEvent and AuditLog entries.
    """
    source = db.get(CapTableEntry, from_entry_id)
    dest = db.get(CapTableEntry, to_entry_id)

    if not source or not dest:
        raise ValueError("Source or destination cap table entry does not exist")
    if source.venture_id != venture_id or dest.venture_id != venture_id:
        raise ValueError("Entries do not belong to the specified venture")
    if equity_pct <= 0:
        raise ValueError("Equity percentage to transfer must be positive")
    if source.equity_pct < equity_pct:
        raise ValueError(f"Insufficient equity in source entry ({source.equity_pct}% < {equity_pct}%)")

    # Perform transfer
    source.equity_pct = round(source.equity_pct - equity_pct, 4)
    dest.equity_pct = round(dest.equity_pct + equity_pct, 4)
    now = utcnow()
    source.updated_at = now
    dest.updated_at = now

    # Verify integrity before finalizing
    total_pct = sum(
        e.equity_pct
        for e in db.scalars(
            select(CapTableEntry).where(CapTableEntry.venture_id == venture_id)
        ).all()
    )
    if not math.isclose(total_pct, 100.0, abs_tol=0.001):
        raise ValueError(f"Cap table integrity violation: total sum would be {total_pct}% instead of 100.0%")

    import uuid
    uid = uuid.uuid4().hex[:12]

    # Record restructuring event
    event = RestructuringEvent(
        id=f"rst_{uid}",
        venture_id=venture_id,
        type="equity_reallocation",
        from_user_id=source.holder_user_id,
        to_user_id=dest.holder_user_id,
        equity_delta_pct=equity_pct,
        stage=stage,
        note=note or f"Transferred {equity_pct}% equity from {source.holder_label} to {dest.holder_label}",
        executed_at=now,
        created_at=now,
    )
    db.add(event)

    # Record audit log
    audit = AuditLog(
        id=f"aud_{uuid.uuid4().hex[:12]}",
        actor_id=actor_id,
        action="equity_reallocation",
        entity="cap_table_entries",
        entity_id=venture_id,
        payload={
            "from_entry_id": from_entry_id,
            "to_entry_id": to_entry_id,
            "equity_pct": equity_pct,
            "note": note,
        },
        created_at=now,
    )
    db.add(audit)

    db.commit()
    db.refresh(event)
    return event
