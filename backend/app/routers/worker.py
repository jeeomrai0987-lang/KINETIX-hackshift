import uuid
import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.db import get_db, models
from backend.app.auth import require_role
from backend.app.schemas.base import ListResponse
from backend.app.schemas.auth import UserResponse
from backend.app.schemas.worker import (
    WorkerDashboardResponse, WorkerProfileUpdate, WorkerSettingsUpdate, WorkerOpportunity
)
from backend.app.schemas.match import InvitationResponse
from backend.app.schemas.challenge import ProofReportResponse
from backend.app.services.cap_table_service import execute_accept_invitation
from backend.app.services.audit_service import log_audit

router = APIRouter(tags=["Worker"])

def user_to_response(u: models.User) -> UserResponse:
    worker_p = None
    if u.worker_profile:
        worker_p = {
            "experienceLevel": u.worker_profile.experience_level,
            "skills": u.worker_profile.skills or [],
            "portfolioUrl": u.worker_profile.portfolio_url,
            "githubUrl": u.worker_profile.github_url,
            "phone": u.worker_profile.phone,
            "whatsappEnabled": u.worker_profile.whatsapp_enabled,
            "cloaked": u.worker_profile.cloaked,
            "weeklyAvailabilityHours": u.worker_profile.weekly_availability_hours,
            "percentile": u.worker_profile.percentile,
        }
    return UserResponse(
        id=u.id,
        name=u.name,
        email=u.email,
        role=u.role,
        title=u.title,
        avatar_url=u.avatar_url,
        node_id=u.node_id,
        verified=u.verified,
        cohort_id=u.cohort_id,
        worker_profile=worker_p,
        created_at=u.created_at
    )

@router.get("/worker/dashboard", response_model=WorkerDashboardResponse)
def get_worker_dashboard(
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    profile = current_user.worker_profile
    percentile = profile.percentile if profile else 96

    active_chgs = db.query(models.Challenge).filter(models.Challenge.status == "open").count()
    pending_invs = db.query(models.Invitation).filter(
        models.Invitation.worker_id == current_user.id,
        models.Invitation.status == "pending"
    ).count()
    proofs = db.query(models.ProofReport).filter(
        models.ProofReport.worker_id == current_user.id
    ).count()

    return WorkerDashboardResponse(
        user=user_to_response(current_user),
        percentile=percentile,
        active_challenges_count=active_chgs,
        pending_invitations_count=pending_invs,
        proof_reports_count=proofs,
        telemetry={
            "benchmarksAttested": proofs,
            "p99AverageMs": 1.84,
            "rank": f"Top {100 - percentile}%",
            "cloakingStatus": "Active" if (profile and profile.cloaked) else "Public"
        }
    )

@router.get("/worker/profile", response_model=UserResponse)
def get_worker_profile(
    current_user: models.User = Depends(require_role("worker"))
):
    return user_to_response(current_user)

@router.put("/worker/profile", response_model=UserResponse)
def update_worker_profile(
    req: WorkerProfileUpdate,
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    if req.name is not None: current_user.name = req.name
    if req.title is not None: current_user.title = req.title

    p = current_user.worker_profile
    if not p:
        p = models.WorkerProfile(user_id=current_user.id)
        db.add(p)

    if req.experience_level is not None: p.experience_level = req.experience_level
    if req.skills is not None: p.skills = req.skills
    if req.portfolio_url is not None: p.portfolio_url = req.portfolio_url
    if req.github_url is not None: p.github_url = req.github_url
    if req.phone is not None: p.phone = req.phone
    if req.whatsapp_enabled is not None: p.whatsapp_enabled = req.whatsapp_enabled
    if req.cloaked is not None: p.cloaked = req.cloaked
    if req.weekly_availability_hours is not None: p.weekly_availability_hours = req.weekly_availability_hours

    log_audit(db, actor_id=current_user.id, action="profile_updated", entity="user", entity_id=current_user.id)
    db.commit()
    db.refresh(current_user)
    return user_to_response(current_user)

@router.get("/worker/settings")
def get_worker_settings(
    current_user: models.User = Depends(require_role("worker"))
):
    p = current_user.worker_profile
    return {
        "cloaked": p.cloaked if p else True,
        "whatsappEnabled": p.whatsapp_enabled if p else False,
        "phone": p.phone if p else "",
        "weeklyAvailabilityHours": p.weekly_availability_hours if p else 40
    }

@router.put("/worker/settings")
def update_worker_settings(
    req: WorkerSettingsUpdate,
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    p = current_user.worker_profile
    if not p:
        p = models.WorkerProfile(user_id=current_user.id)
        db.add(p)

    if req.cloaked is not None: p.cloaked = req.cloaked
    if req.whatsapp_enabled is not None: p.whatsapp_enabled = req.whatsapp_enabled
    if req.phone is not None: p.phone = req.phone
    if req.weekly_availability_hours is not None: p.weekly_availability_hours = req.weekly_availability_hours

    db.commit()
    return {
        "cloaked": p.cloaked,
        "whatsappEnabled": p.whatsapp_enabled,
        "phone": p.phone,
        "weeklyAvailabilityHours": p.weekly_availability_hours
    }

@router.get("/worker/opportunities", response_model=ListResponse[WorkerOpportunity])
def get_worker_opportunities(
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    roles = db.query(models.SquadRole).filter(models.SquadRole.status == "vacant").all()
    items = []
    for r in roles:
        v = r.venture
        app = db.query(models.Application).filter(
            models.Application.role_id == r.id,
            models.Application.worker_id == current_user.id
        ).first()

        blind_token = app.blind_token if app else f"BLIND-{uuid.uuid4().hex[:6].upper()}"
        synergy = 93 + (hash(r.id + current_user.id) % 6)

        items.append(WorkerOpportunity(
            role_id=r.id,
            venture_id=v.id if v else "",
            venture_name=v.name if v else "Emerging AI Venture",
            venture_sector=v.sector if v else "DeepTech",
            role_title=r.title,
            description=r.description or "Lead core architecture implementation.",
            equity_pct=r.equity_pct,
            requirements=r.requirements or [],
            blind_token=blind_token,
            synergy_score=synergy,
            applied=app is not None
        ))

    return ListResponse(items=items, total=len(items))

@router.post("/worker/opportunities/refresh")
def refresh_worker_opportunities(
    current_user: models.User = Depends(require_role("worker"))
):
    return {"message": "Opportunities pipeline refreshed"}

@router.post("/worker/opportunities/{role_id}/apply")
def apply_to_opportunity(
    role_id: str,
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    role = db.query(models.SquadRole).filter(models.SquadRole.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Role not found"}}
        )

    existing = db.query(models.Application).filter(
        models.Application.role_id == role_id,
        models.Application.worker_id == current_user.id
    ).first()

    if existing:
        return {"message": "Application already submitted", "blindToken": existing.blind_token}

    token = f"BLIND-APP-{uuid.uuid4().hex[:8].upper()}"
    app = models.Application(
        id=f"app_{uuid.uuid4().hex[:12]}",
        role_id=role_id,
        worker_id=current_user.id,
        blind_token=token,
        status="submitted"
    )
    db.add(app)
    log_audit(
        db, actor_id=current_user.id, action="application_submitted",
        entity="application", entity_id=app.id,
        payload={"roleId": role_id, "blindToken": token}
    )
    db.commit()
    return {"message": "Application submitted with zero-bias blind token", "blindToken": token}

@router.get("/worker/invitations", response_model=ListResponse[InvitationResponse])
def get_worker_invitations(
    status: Optional[str] = Query(None),
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    query = db.query(models.Invitation).filter(models.Invitation.worker_id == current_user.id)
    if status:
        query = query.filter(models.Invitation.status == status)
    invs = query.all()

    items = []
    for inv in invs:
        v = inv.venture
        r = inv.role
        items.append(InvitationResponse(
            id=inv.id,
            venture_id=inv.venture_id,
            venture_name=v.name if v else None,
            role_id=inv.role_id,
            role_title=r.title if r else None,
            worker_id=inv.worker_id,
            candidate_code=current_user.node_id or "TX-CANDIDATE",
            worker_name=current_user.name if inv.status == "accepted" else None,
            worker_email=current_user.email if inv.status == "accepted" else None,
            equity_pct=inv.equity_pct,
            terms=inv.terms,
            message=inv.message,
            status=inv.status,
            responded_at=inv.responded_at,
            created_at=inv.created_at
        ))

    return ListResponse(items=items, total=len(items))

@router.post("/invitations/{id}/accept", response_model=InvitationResponse)
def accept_invitation(
    id: str,
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    inv = execute_accept_invitation(invitation_id=id, worker_id=current_user.id, db=db)
    v = inv.venture
    r = inv.role
    return InvitationResponse(
        id=inv.id,
        venture_id=inv.venture_id,
        venture_name=v.name if v else None,
        role_id=inv.role_id,
        role_title=r.title if r else None,
        worker_id=inv.worker_id,
        candidate_code=current_user.node_id,
        worker_name=current_user.name,
        worker_email=current_user.email,
        equity_pct=inv.equity_pct,
        terms=inv.terms,
        message=inv.message,
        status=inv.status,
        responded_at=inv.responded_at,
        created_at=inv.created_at
    )

@router.post("/invitations/{id}/decline", response_model=InvitationResponse)
def decline_invitation(
    id: str,
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    inv = db.query(models.Invitation).filter(
        models.Invitation.id == id,
        models.Invitation.worker_id == current_user.id
    ).first()

    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Invitation not found"}}
        )

    inv.status = "declined"
    inv.responded_at = datetime.datetime.utcnow()
    log_audit(
        db, actor_id=current_user.id, action="invitation_declined",
        entity="invitation", entity_id=inv.id,
        payload={"ventureId": inv.venture_id, "roleId": inv.role_id}
    )
    db.commit()
    db.refresh(inv)

    v = inv.venture
    r = inv.role
    return InvitationResponse(
        id=inv.id,
        venture_id=inv.venture_id,
        venture_name=v.name if v else None,
        role_id=inv.role_id,
        role_title=r.title if r else None,
        worker_id=inv.worker_id,
        candidate_code=current_user.node_id,
        equity_pct=inv.equity_pct,
        terms=inv.terms,
        message=inv.message,
        status=inv.status,
        responded_at=inv.responded_at,
        created_at=inv.created_at
    )

@router.get("/worker/proof-of-work", response_model=ListResponse[ProofReportResponse])
def get_worker_proof_of_work(
    current_user: models.User = Depends(require_role("worker")),
    db: Session = Depends(get_db)
):
    reports = db.query(models.ProofReport).filter(
        models.ProofReport.worker_id == current_user.id
    ).all()

    return ListResponse(
        items=[
            ProofReportResponse(
                id=rep.id,
                worker_id=rep.worker_id,
                submission_id=rep.submission_id,
                sprint_name=rep.sprint_name,
                completed_at=rep.completed_at,
                score=rep.score,
                cohort_rank=rep.cohort_rank,
                hash=rep.hash,
                tests_passed=rep.tests_passed,
                tests_total=rep.tests_total,
                p99_latency_ms=rep.p99_latency_ms,
                memory_leak_bytes=rep.memory_leak_bytes,
                reviewer_verdict=rep.reviewer_verdict,
                created_at=rep.created_at
            ) for rep in reports
        ],
        total=len(reports)
    )
