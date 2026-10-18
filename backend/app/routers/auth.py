import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import User, WorkerProfile, InvestorProfile, Cohort, AuditLog
from backend.app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from backend.app.auth import hash_password, verify_password, create_access_token, get_current_user
from backend.app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "EMAIL_EXISTS", "message": "A user with this email address already exists"}}
        )

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    node_id = f"NODE-{req.role.upper()[:3]}-{uuid.uuid4().hex[:4].upper()}"

    # Default cohort
    default_cohort = db.query(Cohort).first()
    cohort_id = default_cohort.id if default_cohort else None

    new_user = User(
        id=user_id,
        email=req.email.lower().strip(),
        password_hash=hash_password(req.password),
        name=req.name.strip(),
        role=req.role.lower(),
        title=req.title or (f"{req.role.capitalize()} / Cohort Alpha"),
        node_id=node_id,
        verified=True,
        cohort_id=cohort_id
    )
    db.add(new_user)
    db.flush()

    if req.role == "worker":
        db.add(WorkerProfile(
            user_id=new_user.id,
            experience_level=req.experience_level or "mid",
            skills=req.skills or [],
            portfolio_url=req.portfolio_url,
            whatsapp_enabled=req.whatsapp_enabled if req.whatsapp_enabled is not None else True,
            cloaked=True,
            weekly_availability_hours=20,
            percentile=92.0
        ))
    elif req.role == "investor":
        db.add(InvestorProfile(
            user_id=new_user.id,
            tier="Syndicate Member",
            preferred_sectors=["Enterprise AI", "Fintech Infrastructure"],
            instant_alerts=True,
            weekly_digest=True,
            accreditation_status="verified"
        ))

    db.add(AuditLog(
        id=f"aud_{uuid.uuid4().hex[:12]}",
        actor_id=new_user.id,
        action="user_registered",
        entity="user",
        entity_id=new_user.id,
        payload={"email": new_user.email, "role": new_user.role}
    ))
    db.commit()

    token = create_access_token(new_user.id, new_user.role)
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email address or password"}}
        )

    token = create_access_token(user.id, user.role)
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user)
    )


@router.post("/demo/{role}", response_model=AuthResponse)
def demo_login(role: str, db: Session = Depends(get_db)):
    if settings.ENV == "production":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": {"code": "DEMO_DISABLED", "message": "Demo login is disabled in production"}}
        )

    role = role.lower()
    demo_id_map = {
        "founder": "usr_founder_01",
        "investor": "usr_investor_02",
        "worker": "usr_worker_03",
        "talent": "usr_worker_03"
    }

    target_id = demo_id_map.get(role)
    if not target_id:
        user = db.query(User).filter(User.role == role).first()
    else:
        user = db.query(User).filter(User.id == target_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "DEMO_USER_NOT_FOUND", "message": f"Demo user for role '{role}' not found"}}
        )

    token = create_access_token(user.id, user.role)
    return AuthResponse(
        token=token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)
