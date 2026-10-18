import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from database.models.core import User
from database.models.venture import SquadRole, Venture
from database.models.worker_profile import WorkerProfile
from database.models.worker_activity import Invitation, ProofReport, Submission, Application


def get_worker_profile(db: Session, user_id: str) -> Optional[WorkerProfile]:
    """Retrieves worker profile for a given user ID."""
    return db.query(WorkerProfile).filter(WorkerProfile.user_id == user_id).first()


def update_worker_profile(db: Session, user_id: str, updates: dict) -> Optional[WorkerProfile]:
    """Updates fields on an existing worker profile."""
    profile = get_worker_profile(db, user_id)
    if not profile:
        return None
    for field, val in updates.items():
        if hasattr(profile, field):
            setattr(profile, field, val)
    db.flush()
    return profile


def get_worker_dashboard_data(db: Session, worker_id: str) -> Optional[Dict[str, Any]]:
    """Aggregates dashboard metrics and telemetry strictly scoped to a worker_id (Role Isolation Rule #4)."""
    user = db.query(User).filter(User.id == worker_id, User.role == "worker").first()
    if not user:
        return None

    profile = get_worker_profile(db, worker_id)
    invitations = db.query(Invitation).filter(Invitation.worker_id == worker_id).order_by(Invitation.created_at.desc()).all()
    pending_invites = [i for i in invitations if i.status == "pending"]
    reports = db.query(ProofReport).filter(ProofReport.worker_id == worker_id).order_by(ProofReport.completed_at.desc()).all()
    submissions = db.query(Submission).filter(Submission.worker_id == worker_id).order_by(Submission.created_at.desc()).all()

    percentile = profile.percentile if profile else 95.0
    top_pct = max(1, 100 - int(percentile))

    return {
        "worker_id": worker_id,
        "user": user,
        "profile": profile,
        "standing": f"Top {top_pct}% (Sprint Alpha)",
        "percentile": percentile,
        "active_challenges_count": len(submissions),
        "pending_invitations_count": len(pending_invites),
        "total_proof_reports": len(reports),
        "recent_invitations": invitations[:3],
        "recent_reports": reports[:3],
        "skills": profile.skills if profile else [],
        "cloaked": profile.cloaked if profile else True,
        "whatsapp_enabled": profile.whatsapp_enabled if profile else True,
    }


def list_worker_invitations(db: Session, worker_id: str, status: Optional[str] = None) -> List[Invitation]:
    """Retrieves invitations addressed to a specific worker, optionally filtered by status (Rule #4)."""
    query = db.query(Invitation).filter(Invitation.worker_id == worker_id)
    if status and status != "all":
        query = query.filter(Invitation.status == status)
    return query.order_by(Invitation.created_at.desc()).all()


def get_worker_invitations(db: Session, worker_id: str, status: Optional[str] = None) -> List[Invitation]:
    """Alias for list_worker_invitations."""
    return list_worker_invitations(db, worker_id, status=status)


def list_open_opportunities(db: Session, worker_id: str) -> List[Dict[str, Any]]:
    """Lists available vacant squad openings with application state scoped for worker_id."""
    applied_role_ids = {
        app.role_id for app in db.query(Application.role_id).filter(Application.worker_id == worker_id).all()
    }
    vacant_roles = db.query(SquadRole).filter(SquadRole.status == "vacant").all()

    opportunities = []
    for role in vacant_roles:
        v = role.venture
        opportunities.append({
            "id": role.id,
            "role_id": role.id,
            "venture_id": role.venture_id,
            "venture_name": v.name if v else "Venture Squad",
            "sector": v.sector if v else "Deep Tech",
            "stage": v.stage if v else "Pre-Seed",
            "thesis": v.thesis if v else "",
            "founder_name": v.founder.name if v and v.founder else "Founder",
            "title": role.title,
            "description": role.description,
            "equity_pct": role.equity_pct,
            "requirements": role.requirements or [],
            "status": role.status,
            "has_applied": role.id in applied_role_ids,
            "role": role,
        })
    return opportunities


def get_proof_of_work(db: Session, worker_id: str, report_id: Optional[str] = None) -> Any:
    """Retrieves one or all proof-of-work cryptographic reports scoped strictly to worker_id."""
    if report_id:
        return db.query(ProofReport).filter(
            ProofReport.id == report_id,
            ProofReport.worker_id == worker_id
        ).first()
    return db.query(ProofReport).filter(
        ProofReport.worker_id == worker_id
    ).order_by(ProofReport.completed_at.desc()).all()


def get_worker_proof_reports(db: Session, worker_id: str) -> List[ProofReport]:
    """Retrieves cryptographic proof-of-work attestations for a worker."""
    return get_proof_of_work(db, worker_id=worker_id)


def get_worker_submissions(db: Session, worker_id: str) -> List[Submission]:
    """Retrieves all sprint challenge submissions for a worker."""
    return db.query(Submission).filter(Submission.worker_id == worker_id).order_by(Submission.created_at.desc()).all()


def get_worker_applications(db: Session, worker_id: str) -> List[Application]:
    """Retrieves blind token applications submitted by a worker."""
    return db.query(Application).filter(Application.worker_id == worker_id).order_by(Application.created_at.desc()).all()
