import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.db import get_db, models
from backend.app.auth import hash_password, verify_password, create_access_token, get_current_user, get_model
from backend.app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from backend.app.services.audit_service import log_audit

router = APIRouter(prefix="/auth", tags=["Auth"])

DEMO_USER_EMAILS = {
    "founder": "alex.mercer@synthetix.ai",
    "investor": "marcus.vance@angelsyndicate.vc",
    "worker": "elena.vance@startup.io"
}

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

    investor_p = None
    if u.investor_profile:
        investor_p = {
            "tier": u.investor_profile.tier,
            "walletAddress": u.investor_profile.wallet_address,
            "preferredSectors": u.investor_profile.preferred_sectors or [],
            "instantAlerts": u.investor_profile.instant_alerts,
            "weeklyDigest": u.investor_profile.weekly_digest,
            "accreditationStatus": u.investor_profile.accreditation_status,
            "accreditationExpiresAt": u.investor_profile.accreditation_expires_at,
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
        investor_profile=investor_p,
        created_at=u.created_at
    )

@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db = Depends(get_db)):
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": {"code": "database_unavailable", "message": "Database layer not connected yet."}}
        )

    User = get_model("User") or getattr(models, "User", None)
    existing = db.query(User).filter(User.email == req.email.lower()).first() if User else None
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "email_taken", "message": "Email address already registered"}}
        )

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    pw_hash = hash_password(req.password)
    node_id = f"NODE-{req.role[:3].upper()}-{uuid.uuid4().hex[:4].upper()}"

    new_user = User(
        id=user_id,
        name=req.name,
        email=req.email.lower(),
        password_hash=pw_hash,
        role=req.role,
        title=req.title or f"{req.role.capitalize()} / Cohort Alpha",
        node_id=node_id,
        verified=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.flush()

    if req.role == "worker":
        WorkerProfile = get_model("WorkerProfile") or getattr(models, "WorkerProfile", None)
        if WorkerProfile:
            profile = WorkerProfile(
                user_id=new_user.id,
                experience_level=req.experience_level or "mid",
                skills=req.skills or [],
                portfolio_url=req.portfolio_url,
                github_url=req.github_url,
                whatsapp_enabled=bool(req.whatsapp_enabled),
                cloaked=True,
                percentile=95
            )
            db.add(profile)
    elif req.role == "investor":
        InvestorProfile = get_model("InvestorProfile") or getattr(models, "InvestorProfile", None)
        if InvestorProfile:
            profile = InvestorProfile(
                user_id=new_user.id,
                tier="Angel Investor",
                preferred_sectors=["Autonomous Agents", "Enterprise Infrastructure"],
                instant_alerts=True,
                weekly_digest=True,
                accreditation_status="verified",
                accreditation_expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)
            )
            db.add(profile)
    elif req.role == "founder":
        Venture = get_model("Venture") or getattr(models, "Venture", None)
        if Venture:
            shell_venture = Venture(
                id=f"ven_{uuid.uuid4().hex[:12]}",
                founder_id=new_user.id,
                name=f"{new_user.name}'s Venture",
                thesis="Autonomous venture thesis pending decomposition.",
                sector="AI & Autonomous Agents",
                stage="Formation",
                clarity_score=0,
                constraints={},
                raised_cents=0,
                runway_months=12,
                mrr_cents=0,
                status="draft",
                created_at=datetime.datetime.utcnow()
            )
            db.add(shell_venture)

    log_audit(db, actor_id=new_user.id, action="user_registered", entity="user", entity_id=new_user.id)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "role": new_user.role, "email": new_user.email})
    return AuthResponse(token=token, user=user_to_response(new_user))

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db = Depends(get_db)):
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": {"code": "database_unavailable", "message": "Database layer not connected yet."}}
        )

    User = get_model("User") or getattr(models, "User", None)
    user = db.query(User).filter(User.email == req.email.lower()).first() if User else None
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "invalid_credentials", "message": "Invalid email or password"}}
        )

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email})
    return AuthResponse(token=token, user=user_to_response(user))

@router.post("/demo/{role}", response_model=AuthResponse)
def demo_login(role: str, db = Depends(get_db)):
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": {"code": "demo_disabled", "message": "Demo login is disabled in production"}}
        )

    target_email = DEMO_USER_EMAILS.get(role.lower())
    if not target_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "invalid_role", "message": f"Demo role '{role}' not found. Available: founder, worker, investor"}}
        )

    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": {"code": "database_unavailable", "message": "Database layer not connected yet."}}
        )

    User = get_model("User") or getattr(models, "User", None)
    user = db.query(User).filter(User.email == target_email).first() if User else None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "user_not_found", "message": f"Demo user for {role} not found in database"}}
        )

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email})
    return AuthResponse(token=token, user=user_to_response(user))

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return user_to_response(current_user)
