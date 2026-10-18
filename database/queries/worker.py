from typing import List, Optional
from sqlalchemy.orm import Session
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


def get_worker_invitations(db: Session, worker_id: str, status: Optional[str] = None) -> List[Invitation]:
    """Retrieves pending or all invitations addressed to a worker."""
    query = db.query(Invitation).filter(Invitation.worker_id == worker_id)
    if status:
        query = query.filter(Invitation.status == status)
    return query.order_by(Invitation.created_at.desc()).all()


def get_worker_proof_reports(db: Session, worker_id: str) -> List[ProofReport]:
    """Retrieves cryptographic proof-of-work attestations for a worker."""
    return db.query(ProofReport).filter(ProofReport.worker_id == worker_id).order_by(ProofReport.completed_at.desc()).all()


def get_worker_submissions(db: Session, worker_id: str) -> List[Submission]:
    """Retrieves all sprint challenge submissions for a worker."""
    return db.query(Submission).filter(Submission.worker_id == worker_id).order_by(Submission.created_at.desc()).all()


def get_worker_applications(db: Session, worker_id: str) -> List[Application]:
    """Retrieves blind token applications submitted by a worker."""
    return db.query(Application).filter(Application.worker_id == worker_id).order_by(Application.created_at.desc()).all()
