import uuid
import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import (
    User, WorkerProfile, Invitation, ProofReport, SquadRole, Application,
    CapTableEntry, AuditLog, Venture
)
from backend.app.auth import require_role
from backend.app.schemas.worker import (
    WorkerProfileUpdate, WorkerSettingsUpdate, OpportunityApplyRequest
)

router = APIRouter(tags=["worker"])


@router.get("/worker/dashboard")
def get_worker_dashboard(
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    prof = db.query(WorkerProfile).filter(WorkerProfile.user_id == user.id).first()
    pending_invites = db.query(Invitation).filter(
        Invitation.worker_id == user.id,
        Invitation.status == "pending"
    ).all()
    reports = db.query(ProofReport).filter(ProofReport.worker_id == user.id).all()

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "nodeId": user.node_id,
            "title": user.title,
            "avatarUrl": user.avatar_url,
            "verified": user.verified
        },
        "percentile": prof.percentile if prof else 96.4,
        "standing": "Top 4% (Sprint Alpha)",
        "activeChallenges": 1,
        "pendingInvitationsCount": len(pending_invites),
        "totalProofReports": len(reports),
        "skills": prof.skills if prof else [],
        "whatsappEnabled": prof.whatsapp_enabled if prof else True,
        "cloaked": prof.cloaked if prof else True
    }


@router.get("/worker/profile")
def get_worker_profile(
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    prof = db.query(WorkerProfile).filter(WorkerProfile.user_id == user.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail={"error": {"code": "PROFILE_NOT_FOUND", "message": "Worker profile not found"}})

    return {
        "userId": user.id,
        "name": user.name,
        "email": user.email,
        "nodeId": user.node_id,
        "title": user.title,
        "avatarUrl": user.avatar_url,
        "experienceLevel": prof.experience_level,
        "skills": prof.skills,
        "portfolioUrl": prof.portfolio_url,
        "githubUrl": prof.github_url,
        "phone": prof.phone,
        "whatsappEnabled": prof.whatsapp_enabled,
        "cloaked": prof.cloaked,
        "weeklyAvailabilityHours": prof.weekly_availability_hours,
        "percentile": prof.percentile
    }


@router.put("/worker/profile")
def update_worker_profile(
    req: WorkerProfileUpdate,
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    prof = db.query(WorkerProfile).filter(WorkerProfile.user_id == user.id).first()
    if not prof:
        raise HTTPException(status_code=404, detail={"error": {"code": "PROFILE_NOT_FOUND", "message": "Worker profile not found"}})

    if req.experience_level is not None: prof.experience_level = req.experience_level
    if req.skills is not None: prof.skills = req.skills
    if req.portfolio_url is not None: prof.portfolio_url = req.portfolio_url
    if req.github_url is not None: prof.github_url = req.github_url
    if req.phone is not None: prof.phone = req.phone
    if req.whatsapp_enabled is not None: prof.whatsapp_enabled = req.whatsapp_enabled
    if req.cloaked is not None: prof.cloaked = req.cloaked
    if req.weekly_availability_hours is not None: prof.weekly_availability_hours = req.weekly_availability_hours

    db.commit()
    return {"status": "success", "message": "Profile updated successfully"}


@router.get("/worker/settings")
def get_worker_settings(
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    prof = db.query(WorkerProfile).filter(WorkerProfile.user_id == user.id).first()
    return {
        "cloaked": prof.cloaked if prof else True,
        "whatsappEnabled": prof.whatsapp_enabled if prof else True,
        "weeklyAvailabilityHours": prof.weekly_availability_hours if prof else 20,
        "phone": prof.phone if prof else "",
        "githubUrl": prof.github_url if prof else ""
    }


@router.put("/worker/settings")
def update_worker_settings(
    req: WorkerSettingsUpdate,
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    prof = db.query(WorkerProfile).filter(WorkerProfile.user_id == user.id).first()
    if prof:
        if req.cloaked is not None: prof.cloaked = req.cloaked
        if req.whatsapp_enabled is not None: prof.whatsapp_enabled = req.whatsapp_enabled
        if req.weekly_availability_hours is not None: prof.weekly_availability_hours = req.weekly_availability_hours
        if req.phone is not None: prof.phone = req.phone
        if req.githubUrl is not None: prof.github_url = req.githubUrl
        db.commit()
    return {"status": "success", "message": "Settings updated"}


@router.get("/worker/opportunities")
def get_worker_opportunities(
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    # Available vacant squad roles
    vacant_roles = db.query(SquadRole).filter(SquadRole.status == "vacant").all()
    items = []
    for r in vacant_roles:
        items.append({
            "id": r.id,
            "ventureName": r.venture.name if r.venture else "Venture Squad",
            "sector": r.venture.sector if r.venture else "Deep Tech",
            "title": r.title,
            "description": r.description,
            "equityPct": r.equity_pct,
            "requirements": r.requirements,
            "status": r.status
        })
    return {"items": items, "total": len(items)}


@router.post("/worker/opportunities/refresh")
def refresh_opportunities(
    user: User = Depends(require_role(["worker"]))
):
    return {"status": "success", "message": "AI Matched openings refreshed"}


@router.post("/worker/opportunities/{roleId}/apply")
def apply_to_opportunity(
    roleId: str,
    req: OpportunityApplyRequest,
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    role = db.query(SquadRole).filter(SquadRole.id == roleId).first()
    if not role:
        raise HTTPException(status_code=404, detail={"error": {"code": "ROLE_NOT_FOUND", "message": "Role not found"}})

    app_id = f"app_{uuid.uuid4().hex[:12]}"
    token = req.blind_token or f"TOK-BLIND-{uuid.uuid4().hex[:6].upper()}"

    app = Application(
        id=app_id,
        role_id=role.id,
        worker_id=user.id,
        blind_token=token,
        status="submitted"
    )
    db.add(app)
    db.commit()

    return {"status": "success", "blindToken": token, "message": "Blind application submitted into evaluation pool"}


@router.get("/worker/invitations")
def get_worker_invitations(
    status: Optional[str] = Query(None),
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    query = db.query(Invitation).filter(Invitation.worker_id == user.id)
    if status and status != "all":
        query = query.filter(Invitation.status == status)
    invites = query.order_by(Invitation.created_at.desc()).all()

    items = []
    for inv in invites:
        items.append({
            "id": inv.id,
            "squad": inv.venture.name if inv.venture else "Venture Squad",
            "role": inv.role.title if inv.role else "Core Engineer",
            "equity": f"{inv.equity_pct}% Equity Grant",
            "equityPct": inv.equity_pct,
            "terms": inv.terms,
            "founder": f"{inv.venture.founder.name} (CEO)" if inv.venture and inv.venture.founder else "Founder",
            "message": inv.message,
            "status": inv.status,
            "date": inv.created_at.strftime("%b %d, %Y") if inv.created_at else "Recently"
        })
    return {"items": items, "total": len(items)}


@router.post("/invitations/{id}/accept")
def accept_invitation(
    id: str,
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    inv = db.query(Invitation).filter(Invitation.id == id, Invitation.worker_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404, detail={"error": {"code": "INVITATION_NOT_FOUND", "message": "Invitation not found"}})

    # Single DB transaction updating Invitation status, Role status, and Cap Table integrity
    try:
        inv.status = "accepted"
        inv.responded_at = datetime.datetime.now(datetime.timezone.utc)

        # Mark role as filled
        if inv.role:
            inv.role.status = "filled"
            inv.role.filled_by_user_id = user.id

        # Update cap table: transfer equity from option_pool to worker
        v_id = inv.venture_id
        option_pool = db.query(CapTableEntry).filter(
            CapTableEntry.venture_id == v_id,
            CapTableEntry.kind == "option_pool"
        ).first()

        equity_grant = inv.equity_pct
        if option_pool and option_pool.equity_pct >= equity_grant:
            option_pool.equity_pct -= equity_grant

            worker_entry = CapTableEntry(
                id=f"cap_{uuid.uuid4().hex[:12]}",
                venture_id=v_id,
                holder_user_id=user.id,
                holder_label=f"{user.name} ({inv.role.title if inv.role else 'Core Founding Engineer'})",
                equity_pct=equity_grant,
                kind="cofounder",
                vested_pct=25.0
            )
            db.add(worker_entry)

        # Verify sum equals 100.0%
        all_caps = db.query(CapTableEntry).filter(CapTableEntry.venture_id == v_id).all()
        total_equity = sum(c.equity_pct for c in all_caps)
        if abs(total_equity - 100.0) > 0.001:
            raise ValueError(f"Cap table integrity breach: sum is {total_equity}% != 100.0%")

        db.add(AuditLog(
            id=f"aud_{uuid.uuid4().hex[:12]}",
            actor_id=user.id,
            action="invitation_accepted",
            entity="invitation",
            entity_id=inv.id,
            payload={"ventureId": v_id, "equityPct": equity_grant}
        ))
        db.commit()

        return {"status": "success", "message": f"Invitation accepted! Wired into {inv.venture.name if inv.venture else 'venture'} cap table"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "ACCEPT_FAILED", "message": str(e)}}
        )


@router.post("/invitations/{id}/decline")
def decline_invitation(
    id: str,
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    inv = db.query(Invitation).filter(Invitation.id == id, Invitation.worker_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404, detail={"error": {"code": "INVITATION_NOT_FOUND", "message": "Invitation not found"}})

    inv.status = "declined"
    inv.responded_at = datetime.datetime.now(datetime.timezone.utc)

    db.add(AuditLog(
        id=f"aud_{uuid.uuid4().hex[:12]}",
        actor_id=user.id,
        action="invitation_declined",
        entity="invitation",
        entity_id=inv.id,
        payload={"ventureId": inv.venture_id}
    ))
    db.commit()

    return {"status": "success", "message": "Invitation declined"}


@router.get("/worker/proof-of-work")
def get_worker_proof_of_work(
    user: User = Depends(require_role(["worker"])),
    db: Session = Depends(get_db)
):
    reports = db.query(ProofReport).filter(ProofReport.worker_id == user.id).order_by(ProofReport.completed_at.desc()).all()
    items = []
    for r in reports:
        items.append({
            "id": r.id,
            "sprint": r.sprint_name,
            "date": f"Completed {r.completed_at.strftime('%b %d, %Y')}",
            "score": f"{r.score} / 100",
            "standing": r.cohort_rank,
            "hash": r.hash,
            "tests": f"{r.tests_passed:,} / {r.tests_total:,} Passed",
            "latency": f"{r.p99_latency_ms}ms p99",
            "memoryLeaks": f"{r.memory_leak_bytes} bytes",
            "reviewerVerdict": r.reviewer_verdict
        })
    return {
        "merkleRoot": "0x7F2A83B49CD1019A82BEE9481CFA42099C4E",
        "items": items,
        "total": len(items)
    }
