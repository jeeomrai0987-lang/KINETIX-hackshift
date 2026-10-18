from typing import Optional, Dict, Any
from backend.app.db import models

def serialize_candidate_for_founder(
    worker_user: models.User,
    candidate_code: str,
    invitation_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Enforces Blind Protocol (Section 6 Rule 1).
    A founder never receives real name, email, avatar_url, or phone until
    that candidate's invitation is accepted.
    """
    is_accepted = invitation_status == "accepted"
    profile = worker_user.worker_profile

    skills = profile.skills if profile and profile.skills else []
    experience_level = profile.experience_level if profile else "mid"
    percentile = profile.percentile if profile else 95

    if is_accepted:
        return {
            "workerId": worker_user.id,
            "candidateCode": candidate_code,
            "name": worker_user.name,
            "email": worker_user.email,
            "avatarUrl": worker_user.avatar_url,
            "avatar": worker_user.avatar_url,
            "phone": profile.phone if profile else None,
            "contact": profile.phone if profile else worker_user.email,
            "skills": skills,
            "experienceLevel": experience_level,
            "percentile": percentile,
            "isCloaked": False,
            "revealed": True
        }
    else:
        # Strictly cloaked
        return {
            "workerId": worker_user.id,
            "candidateCode": candidate_code,
            "name": f"Candidate #{candidate_code}",
            "avatar": None,
            "contact": None,
            "skills": skills,
            "experienceLevel": experience_level,
            "percentile": percentile,
            "isCloaked": True,
            "revealed": False
        }
