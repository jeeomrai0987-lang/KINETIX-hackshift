import uuid
import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.app.db import models
from backend.app.services.audit_service import log_audit

TOLERANCE = 0.001

def verify_cap_table_sum(venture_id: str, db: Session) -> float:
    entries = db.query(models.CapTableEntry).filter(
        models.CapTableEntry.venture_id == venture_id
    ).all()
    total = sum(e.equity_pct for e in entries)
    if abs(total - 100.0) > TOLERANCE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "cap_table_imbalance",
                    "message": f"Cap table sum violation: {total:.3f}% (must be 100.0% +/- {TOLERANCE})"
                }
            }
        )
    return total

def execute_accept_invitation(invitation_id: str, worker_id: str, db: Session) -> models.Invitation:
    """
    Accepts invitation, fills squad role, creates cap table entry, and balances equity
    in a SINGLE transaction.
    """
    inv = db.query(models.Invitation).filter(
        models.Invitation.id == invitation_id,
        models.Invitation.worker_id == worker_id
    ).first()

    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Invitation not found"}}
        )

    if inv.status == "accepted":
        return inv

    # Update invitation status
    inv.status = "accepted"
    inv.responded_at = datetime.datetime.utcnow()

    # Update squad role
    role = db.query(models.SquadRole).filter(models.SquadRole.id == inv.role_id).first()
    if role:
        role.status = "filled"
        role.filled_by_user_id = worker_id

    # Cap Table rebalancing:
    # Look for Option Pool or Reserve to deduct from
    pool_entry = db.query(models.CapTableEntry).filter(
        models.CapTableEntry.venture_id == inv.venture_id,
        models.CapTableEntry.kind.in_(["option_pool", "reserve"])
    ).first()

    equity_needed = inv.equity_pct
    if pool_entry and pool_entry.equity_pct >= equity_needed:
        pool_entry.equity_pct = round(pool_entry.equity_pct - equity_needed, 4)
    else:
        # Fallback: deduct from founder's entry
        founder_entry = db.query(models.CapTableEntry).filter(
            models.CapTableEntry.venture_id == inv.venture_id,
            models.CapTableEntry.kind == "founder"
        ).first()
        if founder_entry and founder_entry.equity_pct >= equity_needed:
            founder_entry.equity_pct = round(founder_entry.equity_pct - equity_needed, 4)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"code": "insufficient_equity", "message": "No available equity pool to allocate this invitation."}}
            )

    worker_user = db.query(models.User).filter(models.User.id == worker_id).first()
    worker_label = f"{worker_user.name} ({role.title if role else 'Core Member'})" if worker_user else f"Member ({inv.worker_id})"

    # Check if worker already has an entry
    existing_cap = db.query(models.CapTableEntry).filter(
        models.CapTableEntry.venture_id == inv.venture_id,
        models.CapTableEntry.holder_user_id == worker_id
    ).first()

    if existing_cap:
        existing_cap.equity_pct = round(existing_cap.equity_pct + equity_needed, 4)
    else:
        new_entry = models.CapTableEntry(
            id=f"cap_{uuid.uuid4().hex[:12]}",
            venture_id=inv.venture_id,
            holder_user_id=worker_id,
            holder_label=worker_label,
            equity_pct=round(equity_needed, 4),
            kind="cofounder",
            vested_pct=25.0
        )
        db.add(new_entry)

    db.flush()
    verify_cap_table_sum(inv.venture_id, db)

    # Log audit
    log_audit(
        db=db,
        actor_id=worker_id,
        action="invitation_accepted",
        entity="invitation",
        entity_id=inv.id,
        payload={"equityPct": equity_needed, "ventureId": inv.venture_id, "roleId": inv.role_id}
    )

    db.commit()
    db.refresh(inv)
    return inv

def execute_restructuring(
    venture_id: str,
    actor_id: str,
    type_: str,
    equity_delta_pct: float,
    from_user_id: Optional[str],
    to_user_id: Optional[str],
    stage: str,
    note: Optional[str],
    db: Session
) -> models.RestructuringEvent:
    """
    Executes an equity restructuring event in a single transaction, keeping total at 100.0%.
    """
    # From holder
    from_entry = None
    if from_user_id:
        from_entry = db.query(models.CapTableEntry).filter(
            models.CapTableEntry.venture_id == venture_id,
            models.CapTableEntry.holder_user_id == from_user_id
        ).first()
    else:
        # Default to founder
        from_entry = db.query(models.CapTableEntry).filter(
            models.CapTableEntry.venture_id == venture_id,
            models.CapTableEntry.kind == "founder"
        ).first()

    # To holder
    to_entry = None
    if to_user_id:
        to_entry = db.query(models.CapTableEntry).filter(
            models.CapTableEntry.venture_id == venture_id,
            models.CapTableEntry.holder_user_id == to_user_id
        ).first()
    else:
        # Default to option pool
        to_entry = db.query(models.CapTableEntry).filter(
            models.CapTableEntry.venture_id == venture_id,
            models.CapTableEntry.kind.in_(["option_pool", "reserve"])
        ).first()

    if not from_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "invalid_source", "message": "Source equity holder not found."}}
        )

    if from_entry.equity_pct < equity_delta_pct:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "insufficient_equity", "message": f"Source holder only has {from_entry.equity_pct}% equity."}}
        )

    from_entry.equity_pct = round(from_entry.equity_pct - equity_delta_pct, 4)

    if to_entry:
        to_entry.equity_pct = round(to_entry.equity_pct + equity_delta_pct, 4)
    else:
        # Create option pool entry if not exists
        to_entry = models.CapTableEntry(
            id=f"cap_{uuid.uuid4().hex[:12]}",
            venture_id=venture_id,
            holder_user_id=to_user_id,
            holder_label="Unallocated ESOP Pool",
            equity_pct=round(equity_delta_pct, 4),
            kind="option_pool",
            vested_pct=0.0
        )
        db.add(to_entry)

    rst = models.RestructuringEvent(
        id=f"rst_{uuid.uuid4().hex[:12]}",
        venture_id=venture_id,
        type=type_,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        equity_delta_pct=equity_delta_pct,
        stage=stage,
        note=note,
        executed_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    )
    db.add(rst)
    db.flush()

    verify_cap_table_sum(venture_id, db)

    log_audit(
        db=db,
        actor_id=actor_id,
        action="restructuring_executed",
        entity="restructuring_event",
        entity_id=rst.id,
        payload={"ventureId": venture_id, "deltaPct": equity_delta_pct, "type": type_}
    )

    db.commit()
    db.refresh(rst)
    return rst
