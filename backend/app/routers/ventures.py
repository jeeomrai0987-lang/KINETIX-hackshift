import io
import csv
import uuid
import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from backend.app.db import get_db, models
from backend.app.auth import require_role
from backend.app.schemas.base import ListResponse
from backend.app.schemas.venture import (
    VentureCreate, VentureUpdate, VentureResponse, VentureDashboardResponse,
    DecomposeRequest, DecomposeResponse, BlueprintApproveRequest, SquadRoleSchema
)
from backend.app.schemas.match import MatchResponse, InviteRequest, InvitationResponse
from backend.app.schemas.challenge import (
    ChallengeResponse, SubmissionResponse, ScoreRequest, ProofReportResponse
)
from backend.app.schemas.restructuring import (
    RestructuringExecuteRequest, RestructuringEventResponse
)
from backend.app.schemas.financial import (
    FinancialsOverviewResponse, FinancialSnapshotResponse, TransactionResponse,
    CapTableResponse, CapTableEntryResponse, FundingOpportunityResponse,
    FundingRequestCreate, FundingRequestResponse
)
from backend.app.services.ai_service import decompose_thesis
from backend.app.services.blind_service import serialize_candidate_for_founder
from backend.app.services.hash_service import compute_canonical_hash
from backend.app.services.cap_table_service import (
    verify_cap_table_sum, execute_restructuring
)
from backend.app.services.audit_service import log_audit

router = APIRouter(tags=["Founder"])

# Helper to verify founder ownership
def get_venture_for_founder(venture_id: str, founder_id: str, db: Session) -> models.Venture:
    venture = db.query(models.Venture).filter(
        models.Venture.id == venture_id,
        models.Venture.founder_id == founder_id
    ).first()
    if not venture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Venture not found or access denied"}}
        )
    return venture


# --- Venture CRUD ---

@router.get("/ventures/mine", response_model=ListResponse[VentureResponse])
def get_my_ventures(
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    ventures = db.query(models.Venture).filter(models.Venture.founder_id == current_user.id).all()
    return ListResponse(
        items=[
            VentureResponse(
                id=v.id,
                founder_id=v.founder_id,
                cohort_id=v.cohort_id,
                name=v.name,
                thesis=v.thesis,
                sector=v.sector,
                stage=v.stage,
                clarity_score=v.clarity_score,
                constraints=v.constraints or {},
                raised_cents=v.raised_cents,
                runway_months=v.runway_months,
                mrr_cents=v.mrr_cents,
                status=v.status,
                created_at=v.created_at,
                updated_at=v.updated_at
            ) for v in ventures
        ],
        total=len(ventures)
    )

@router.post("/ventures", response_model=VentureResponse)
def create_venture(
    req: VentureCreate,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    ven_id = f"ven_{uuid.uuid4().hex[:12]}"
    venture = models.Venture(
        id=ven_id,
        founder_id=current_user.id,
        cohort_id=current_user.cohort_id,
        name=req.name,
        thesis=req.thesis,
        sector=req.sector,
        stage=req.stage or "Sprint 3 / Proof-of-Work",
        clarity_score=90,
        constraints=req.constraints or {},
        raised_cents=0,
        runway_months=18,
        mrr_cents=0,
        status="active"
    )
    db.add(venture)

    # Initial cap table entry: 100% to Founder
    cap = models.CapTableEntry(
        id=f"cap_{uuid.uuid4().hex[:12]}",
        venture_id=ven_id,
        holder_user_id=current_user.id,
        holder_label=f"{current_user.name} (Founder / CEO)",
        equity_pct=100.0,
        kind="founder",
        vested_pct=100.0
    )
    db.add(cap)

    log_audit(db, actor_id=current_user.id, action="venture_created", entity="venture", entity_id=ven_id)
    db.commit()
    db.refresh(venture)

    return VentureResponse(
        id=venture.id,
        founder_id=venture.founder_id,
        cohort_id=venture.cohort_id,
        name=venture.name,
        thesis=venture.thesis,
        sector=venture.sector,
        stage=venture.stage,
        clarity_score=venture.clarity_score,
        constraints=venture.constraints or {},
        raised_cents=venture.raised_cents,
        runway_months=venture.runway_months,
        mrr_cents=venture.mrr_cents,
        status=venture.status,
        created_at=venture.created_at,
        updated_at=venture.updated_at
    )

@router.put("/ventures/{id}", response_model=VentureResponse)
def update_venture(
    id: str,
    req: VentureUpdate,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    if req.name is not None: venture.name = req.name
    if req.thesis is not None: venture.thesis = req.thesis
    if req.sector is not None: venture.sector = req.sector
    if req.stage is not None: venture.stage = req.stage
    if req.constraints is not None: venture.constraints = req.constraints
    if req.runway_months is not None: venture.runway_months = req.runway_months
    if req.mrr_cents is not None: venture.mrr_cents = req.mrr_cents
    if req.raised_cents is not None: venture.raised_cents = req.raised_cents
    venture.updated_at = datetime.datetime.utcnow()

    log_audit(db, actor_id=current_user.id, action="venture_updated", entity="venture", entity_id=venture.id)
    db.commit()
    db.refresh(venture)

    return VentureResponse(
        id=venture.id,
        founder_id=venture.founder_id,
        cohort_id=venture.cohort_id,
        name=venture.name,
        thesis=venture.thesis,
        sector=venture.sector,
        stage=venture.stage,
        clarity_score=venture.clarity_score,
        constraints=venture.constraints or {},
        raised_cents=venture.raised_cents,
        runway_months=venture.runway_months,
        mrr_cents=venture.mrr_cents,
        status=venture.status,
        created_at=venture.created_at,
        updated_at=venture.updated_at
    )


# --- Dashboard ---

@router.get("/ventures/{id}/dashboard", response_model=VentureDashboardResponse)
def get_venture_dashboard(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)

    roles = db.query(models.SquadRole).filter(models.SquadRole.venture_id == venture.id).all()
    roster = []
    for r in roles:
        holder_name = "Vacant — Recruiting"
        if r.filled_by:
            holder_name = r.filled_by.name
        roster.append({
            "id": r.id,
            "role": r.title,
            "holder": holder_name,
            "status": r.status,
            "equity": f"{r.equity_pct}%",
            "requirements": r.requirements or []
        })

    feed = [
        {"title": "Arbitrum simulated L2 root state hash published", "time": "12m ago", "tag": "Verification"},
        {"title": "Candidate TX-5512B completed Sprint 3 consensus harness", "time": "1h ago", "tag": "Challenge"},
        {"title": "Angel Syndicate SAFE Tranche 1 approved", "time": "4h ago", "tag": "Funding"},
        {"title": "SOC2 Type II attestation package verified", "time": "1d ago", "tag": "Compliance"}
    ]

    return VentureDashboardResponse(
        venture=VentureResponse(
            id=venture.id,
            founder_id=venture.founder_id,
            cohort_id=venture.cohort_id,
            name=venture.name,
            thesis=venture.thesis,
            sector=venture.sector,
            stage=venture.stage,
            clarity_score=venture.clarity_score,
            constraints=venture.constraints or {},
            raised_cents=venture.raised_cents,
            runway_months=venture.runway_months,
            mrr_cents=venture.mrr_cents,
            status=venture.status,
            created_at=venture.created_at,
            updated_at=venture.updated_at
        ),
        squad_synergy=96,
        runway=f"{venture.runway_months} Months",
        sprint_clock={
            "sprint": "Sprint 3",
            "hoursLeft": 22,
            "totalHours": 48,
            "status": "In Progress"
        },
        roster=roster,
        cohort_feed=feed
    )


# --- Thesis Decomposition & Blueprint ---

@router.post("/ventures/{id}/decompose", response_model=DecomposeResponse)
async def decompose_venture_thesis(
    id: str,
    req: DecomposeRequest,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    result = await decompose_thesis(req.thesis or venture.thesis)
    return DecomposeResponse(
        thesis=result["thesis"],
        constraints=result["constraints"],
        blueprint=result["blueprint"]
    )

@router.post("/ventures/{id}/blueprint/approve")
def approve_blueprint(
    id: str,
    req: BlueprintApproveRequest,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)

    # If roles are provided in body, sync them; else use existing or generate default
    roles_data = req.roles or []
    if not roles_data:
        # Default 2 vacant roles if none exist
        roles_data = [
            {
                "title": "Founding Distributed Systems Engineer",
                "description": "Low-latency consensus engine",
                "equityPct": 15.0,
                "requirements": ["Distributed Systems", "Rust", "Go"]
            },
            {
                "title": "Lead Inference Systems Engineer",
                "description": "vLLM kernels and latency tuning",
                "equityPct": 10.0,
                "requirements": ["CUDA", "PyTorch", "vLLM"]
            }
        ]

    for item in roles_data:
        title = item.title if hasattr(item, "title") else item["title"]
        desc = item.description if hasattr(item, "description") else item.get("description", "")
        eq = item.equity_pct if hasattr(item, "equity_pct") else item.get("equityPct", 15.0)
        reqs = item.requirements if hasattr(item, "requirements") else item.get("requirements", [])

        # Check existing
        existing_role = db.query(models.SquadRole).filter(
            models.SquadRole.venture_id == venture.id,
            models.SquadRole.title == title
        ).first()

        if not existing_role:
            new_role = models.SquadRole(
                id=f"rol_{uuid.uuid4().hex[:12]}",
                venture_id=venture.id,
                title=title,
                description=desc,
                equity_pct=eq,
                status="vacant",
                requirements=reqs
            )
            db.add(new_role)

    log_audit(db, actor_id=current_user.id, action="blueprint_approved", entity="venture", entity_id=venture.id)
    db.commit()

    # Trigger candidate matches
    trigger_match_run(venture.id, db)

    return {"message": "Blueprint approved and match run triggered successfully."}


# --- Matching & Blind Protocol ---

def trigger_match_run(venture_id: str, db: Session):
    vacant_roles = db.query(models.SquadRole).filter(
        models.SquadRole.venture_id == venture_id,
        models.SquadRole.status == "vacant"
    ).all()

    workers = db.query(models.User).filter(models.User.role == "worker").all()

    for role in vacant_roles:
        for w in workers:
            existing_match = db.query(models.Match).filter(
                models.Match.venture_id == venture_id,
                models.Match.role_id == role.id,
                models.Match.worker_id == w.id
            ).first()

            if not existing_match:
                synergy = 92 + (hash(w.id + role.id) % 7)
                code = w.node_id or f"TX-{uuid.uuid4().hex[:4].upper()}"
                m = models.Match(
                    id=f"mat_{uuid.uuid4().hex[:12]}",
                    venture_id=venture_id,
                    role_id=role.id,
                    worker_id=w.id,
                    candidate_code=code,
                    synergy_score=synergy,
                    fit_details={"technicalMatch": synergy + 1, "availabilityMatch": 95},
                    status="suggested"
                )
                db.add(m)
    db.commit()

@router.get("/ventures/{id}/matches", response_model=ListResponse[MatchResponse])
def get_venture_matches(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    matches = db.query(models.Match).filter(models.Match.venture_id == venture.id).all()

    items = []
    for m in matches:
        # Check if invitation was accepted
        inv = db.query(models.Invitation).filter(
            models.Invitation.venture_id == venture.id,
            models.Invitation.worker_id == m.worker_id
        ).first()
        inv_status = inv.status if inv else None

        # Apply Blind Protocol (Section 6 Rule 1)
        serialized = serialize_candidate_for_founder(m.worker, m.candidate_code, inv_status)

        items.append(MatchResponse(
            id=m.id,
            venture_id=m.venture_id,
            role_id=m.role_id,
            role_title=m.role.title if m.role else None,
            worker_id=m.worker_id,
            candidate_code=m.candidate_code,
            synergy_score=m.synergy_score,
            fit_details=m.fit_details or {},
            status=m.status,
            skills=serialized["skills"],
            experience_level=serialized["experienceLevel"],
            percentile=serialized["percentile"],
            name=serialized.get("name"),
            avatar=serialized.get("avatar"),
            contact=serialized.get("contact"),
            is_cloaked=serialized.get("isCloaked", True),
            created_at=m.created_at
        ))

    return ListResponse(items=items, total=len(items))

@router.post("/ventures/{id}/matches/rerun")
def rerun_venture_matches(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    trigger_match_run(venture.id, db)
    log_audit(db, actor_id=current_user.id, action="matches_rerun", entity="venture", entity_id=venture.id)
    return {"message": "Candidate matching engine re-executed successfully"}

@router.post("/matches/{id}/invite", response_model=InvitationResponse)
def invite_candidate(
    id: str,
    req: InviteRequest,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    match = db.query(models.Match).filter(models.Match.id == id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Match not found"}}
        )

    get_venture_for_founder(match.venture_id, current_user.id, db)

    # Check existing invitation
    existing_inv = db.query(models.Invitation).filter(
        models.Invitation.role_id == match.role_id,
        models.Invitation.worker_id == match.worker_id
    ).first()

    if existing_inv:
        return InvitationResponse(
            id=existing_inv.id,
            venture_id=existing_inv.venture_id,
            venture_name=match.venture.name if match.venture else None,
            role_id=existing_inv.role_id,
            role_title=match.role.title if match.role else None,
            worker_id=existing_inv.worker_id,
            candidate_code=match.candidate_code,
            equity_pct=existing_inv.equity_pct,
            terms=existing_inv.terms,
            message=existing_inv.message,
            status=existing_inv.status,
            responded_at=existing_inv.responded_at,
            created_at=existing_inv.created_at
        )

    inv_id = f"inv_{uuid.uuid4().hex[:12]}"
    inv = models.Invitation(
        id=inv_id,
        venture_id=match.venture_id,
        role_id=match.role_id,
        worker_id=match.worker_id,
        equity_pct=req.equity_pct,
        terms=req.terms,
        message=req.message or "We were impressed with your verified benchmarks and want to invite you to join our founding squad.",
        status="pending"
    )
    match.status = "invited"
    db.add(inv)

    log_audit(
        db, actor_id=current_user.id, action="invitation_sent",
        entity="invitation", entity_id=inv.id,
        payload={"ventureId": match.venture_id, "workerId": match.worker_id, "equityPct": req.equity_pct}
    )
    db.commit()
    db.refresh(inv)

    return InvitationResponse(
        id=inv.id,
        venture_id=inv.venture_id,
        venture_name=match.venture.name if match.venture else None,
        role_id=inv.role_id,
        role_title=match.role.title if match.role else None,
        worker_id=inv.worker_id,
        candidate_code=match.candidate_code,
        equity_pct=inv.equity_pct,
        terms=inv.terms,
        message=inv.message,
        status=inv.status,
        responded_at=inv.responded_at,
        created_at=inv.created_at
    )


# --- Challenges & Submissions ---

@router.get("/ventures/{id}/challenge", response_model=ListResponse[ChallengeResponse])
def get_venture_challenges(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    challenges = db.query(models.Challenge).filter(models.Challenge.venture_id == venture.id).all()
    return ListResponse(
        items=[
            ChallengeResponse(
                id=c.id,
                venture_id=c.venture_id,
                role_id=c.role_id,
                title=c.title,
                duration_hours=c.duration_hours,
                starts_at=c.starts_at,
                ends_at=c.ends_at,
                status=c.status,
                created_at=c.created_at
            ) for c in challenges
        ],
        total=len(challenges)
    )

@router.get("/challenges/{id}/submissions", response_model=ListResponse[SubmissionResponse])
def get_challenge_submissions(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    chg = db.query(models.Challenge).filter(models.Challenge.id == id).first()
    if not chg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Challenge not found"}}
        )
    get_venture_for_founder(chg.venture_id, current_user.id, db)

    subs = db.query(models.Submission).filter(models.Submission.challenge_id == chg.id).all()
    return ListResponse(
        items=[
            SubmissionResponse(
                id=s.id,
                challenge_id=s.challenge_id,
                worker_id=s.worker_id,
                candidate_code=s.candidate_code,
                status=s.status,
                score=s.score,
                p99_latency_ms=s.p99_latency_ms,
                tests_passed=s.tests_passed,
                tests_total=s.tests_total,
                hash=s.hash,
                replay_integrity=s.replay_integrity,
                failure_recovery=s.failure_recovery,
                concurrency_latency=s.concurrency_latency,
                code_elegance=s.code_elegance,
                reviewer_verdict=s.reviewer_verdict,
                signed_at=s.signed_at,
                created_at=s.created_at
            ) for s in subs
        ],
        total=len(subs)
    )

@router.post("/submissions/{id}/score", response_model=SubmissionResponse)
def score_submission(
    id: str,
    req: ScoreRequest,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    sub = db.query(models.Submission).filter(models.Submission.id == id).first()
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Submission not found"}}
        )

    # Update multi-vector scores
    scores = req.vector_scores
    if "replayIntegrity" in scores: sub.replay_integrity = float(scores["replayIntegrity"])
    if "failureRecovery" in scores: sub.failure_recovery = float(scores["failureRecovery"])
    if "concurrencyLatency" in scores: sub.concurrency_latency = float(scores["concurrencyLatency"])
    if "codeElegance" in scores: sub.code_elegance = float(scores["codeElegance"])

    composite = (sub.replay_integrity + sub.failure_recovery + sub.concurrency_latency + sub.code_elegance) / 4.0
    sub.score = int(round(composite))
    if req.reviewer_verdict:
        sub.reviewer_verdict = req.reviewer_verdict

    # Compute real SHA-256 canonical hash (Section 6 Rule 2)
    payload_to_hash = {
        "candidate_code": sub.candidate_code,
        "challenge_id": sub.challenge_id,
        "code_elegance": sub.code_elegance,
        "concurrency_latency": sub.concurrency_latency,
        "failure_recovery": sub.failure_recovery,
        "p99_latency_ms": sub.p99_latency_ms,
        "replay_integrity": sub.replay_integrity,
        "reviewer_verdict": sub.reviewer_verdict,
        "score": sub.score,
        "submission_id": sub.id,
        "tests_passed": sub.tests_passed,
        "tests_total": sub.tests_total,
        "worker_id": sub.worker_id,
    }
    sub.hash = compute_canonical_hash(payload_to_hash)

    log_audit(
        db, actor_id=current_user.id, action="submission_scored",
        entity="submission", entity_id=sub.id,
        payload={"score": sub.score, "hash": sub.hash}
    )
    db.commit()
    db.refresh(sub)

    return SubmissionResponse(
        id=sub.id,
        challenge_id=sub.challenge_id,
        worker_id=sub.worker_id,
        candidate_code=sub.candidate_code,
        status=sub.status,
        score=sub.score,
        p99_latency_ms=sub.p99_latency_ms,
        tests_passed=sub.tests_passed,
        tests_total=sub.tests_total,
        hash=sub.hash,
        replay_integrity=sub.replay_integrity,
        failure_recovery=sub.failure_recovery,
        concurrency_latency=sub.concurrency_latency,
        code_elegance=sub.code_elegance,
        reviewer_verdict=sub.reviewer_verdict,
        signed_at=sub.signed_at,
        created_at=sub.created_at
    )

@router.post("/submissions/{id}/sign", response_model=SubmissionResponse)
def sign_submission(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    sub = db.query(models.Submission).filter(models.Submission.id == id).first()
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Submission not found"}}
        )

    sub.status = "attested"
    sub.signed_at = datetime.datetime.utcnow()

    # Re-compute cryptographic attestation hash
    payload_to_hash = {
        "submissionId": sub.id,
        "candidateCode": sub.candidate_code,
        "score": sub.score,
        "p99LatencyMs": sub.p99_latency_ms,
        "testsPassed": sub.tests_passed,
        "testsTotal": sub.tests_total,
        "signedAt": sub.signed_at.isoformat(),
        "attestedBy": current_user.id
    }
    sub.hash = compute_canonical_hash(payload_to_hash)

    # Create or update ProofReport
    proof = db.query(models.ProofReport).filter(models.ProofReport.submission_id == sub.id).first()
    if not proof:
        proof = models.ProofReport(
            id=f"rep_{uuid.uuid4().hex[:12]}",
            worker_id=sub.worker_id,
            submission_id=sub.id,
            sprint_name="Sprint 3 / Distributed Systems Consensus",
            completed_at=sub.signed_at,
            score=sub.score,
            cohort_rank="Top 1%",
            hash=sub.hash,
            tests_passed=sub.tests_passed,
            tests_total=sub.tests_total,
            p99_latency_ms=sub.p99_latency_ms,
            memory_leak_bytes=0,
            reviewer_verdict="Cryptographically signed by founder on Arbitrum simulated testnet."
        )
        db.add(proof)
    else:
        proof.hash = sub.hash
        proof.score = sub.score
        proof.completed_at = sub.signed_at

    log_audit(
        db, actor_id=current_user.id, action="submission_signed",
        entity="submission", entity_id=sub.id,
        payload={"hash": sub.hash, "signedAt": sub.signed_at.isoformat()}
    )
    db.commit()
    db.refresh(sub)

    return SubmissionResponse(
        id=sub.id,
        challenge_id=sub.challenge_id,
        worker_id=sub.worker_id,
        candidate_code=sub.candidate_code,
        status=sub.status,
        score=sub.score,
        p99_latency_ms=sub.p99_latency_ms,
        tests_passed=sub.tests_passed,
        tests_total=sub.tests_total,
        hash=sub.hash,
        replay_integrity=sub.replay_integrity,
        failure_recovery=sub.failure_recovery,
        concurrency_latency=sub.concurrency_latency,
        code_elegance=sub.code_elegance,
        reviewer_verdict=sub.reviewer_verdict,
        signed_at=sub.signed_at,
        created_at=sub.created_at
    )

@router.get("/submissions/{id}/proof", response_model=ProofReportResponse)
def get_submission_proof(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    sub = db.query(models.Submission).filter(models.Submission.id == id).first()
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Submission not found"}}
        )

    proof = db.query(models.ProofReport).filter(models.ProofReport.submission_id == sub.id).first()
    if not proof:
        # Create on demand
        proof = models.ProofReport(
            id=f"rep_{uuid.uuid4().hex[:12]}",
            worker_id=sub.worker_id,
            submission_id=sub.id,
            sprint_name="Sprint 3 / Distributed Systems Consensus",
            completed_at=sub.signed_at or datetime.datetime.utcnow(),
            score=sub.score,
            cohort_rank="Top 1%",
            hash=sub.hash,
            tests_passed=sub.tests_passed,
            tests_total=sub.tests_total,
            p99_latency_ms=sub.p99_latency_ms,
            memory_leak_bytes=0,
            reviewer_verdict="Cryptographically signed by automated zero-bias test harness."
        )
        db.add(proof)
        db.commit()
        db.refresh(proof)

    return ProofReportResponse(
        id=proof.id,
        worker_id=proof.worker_id,
        submission_id=proof.submission_id,
        sprint_name=proof.sprint_name,
        completed_at=proof.completed_at,
        score=proof.score,
        cohort_rank=proof.cohort_rank,
        hash=proof.hash,
        tests_passed=proof.tests_passed,
        tests_total=proof.tests_total,
        p99_latency_ms=proof.p99_latency_ms,
        memory_leak_bytes=proof.memory_leak_bytes,
        reviewer_verdict=proof.reviewer_verdict,
        created_at=proof.created_at
    )


# --- Restructuring ---

@router.get("/ventures/{id}/restructuring", response_model=ListResponse[RestructuringEventResponse])
def get_restructuring_events(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    events = db.query(models.RestructuringEvent).filter(
        models.RestructuringEvent.venture_id == venture.id
    ).all()

    items = []
    for e in events:
        from_name = e.from_user_id
        to_name = e.to_user_id
        if e.from_user_id:
            u_from = db.query(models.User).filter(models.User.id == e.from_user_id).first()
            if u_from: from_name = u_from.name
        if e.to_user_id:
            u_to = db.query(models.User).filter(models.User.id == e.to_user_id).first()
            if u_to: to_name = u_to.name

        items.append(RestructuringEventResponse(
            id=e.id,
            venture_id=e.venture_id,
            type=e.type,
            from_user_id=e.from_user_id,
            from_user_name=from_name,
            to_user_id=e.to_user_id,
            to_user_name=to_name,
            equity_delta_pct=e.equity_delta_pct,
            stage=e.stage,
            note=e.note,
            executed_at=e.executed_at,
            created_at=e.created_at
        ))

    return ListResponse(items=items, total=len(items))

@router.post("/ventures/{id}/restructuring/execute", response_model=RestructuringEventResponse)
def execute_restructuring_endpoint(
    id: str,
    req: RestructuringExecuteRequest,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    rst = execute_restructuring(
        venture_id=venture.id,
        actor_id=current_user.id,
        type_=req.type,
        equity_delta_pct=req.equity_delta_pct,
        from_user_id=req.from_user_id,
        to_user_id=req.to_user_id,
        stage=req.stage or "Approved",
        note=req.note,
        db=db
    )
    return RestructuringEventResponse(
        id=rst.id,
        venture_id=rst.venture_id,
        type=rst.type,
        from_user_id=rst.from_user_id,
        to_user_id=rst.to_user_id,
        equity_delta_pct=rst.equity_delta_pct,
        stage=rst.stage,
        note=rst.note,
        executed_at=rst.executed_at,
        created_at=rst.created_at
    )


# --- Funding Opportunities ---

@router.get("/ventures/{id}/funding-opportunities", response_model=ListResponse[FundingOpportunityResponse])
def get_funding_opportunities(
    id: str,
    category: Optional[str] = Query(None),
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    query = db.query(models.FundingOpportunity)
    if category:
        query = query.filter(models.FundingOpportunity.category == category)
    opps = query.all()

    items = []
    for op in opps:
        # Check if already requested
        fr = db.query(models.FundingRequest).filter(
            models.FundingRequest.venture_id == venture.id,
            models.FundingRequest.funding_opportunity_id == op.id
        ).first()
        status_val = fr.status if fr else "available"

        items.append(FundingOpportunityResponse(
            id=op.id,
            name=op.name,
            category=op.category,
            check_min_cents=op.check_min_cents,
            check_max_cents=op.check_max_cents,
            structure=op.structure,
            tags=op.tags or [],
            timeline=op.timeline,
            base_fit_pct=op.base_fit_pct,
            status=status_val
        ))
    return ListResponse(items=items, total=len(items))

@router.post("/funding-opportunities/{id}/request", response_model=FundingRequestResponse)
def request_funding_opportunity(
    id: str,
    req: FundingRequestCreate,
    venture_id: str = Query(...),
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(venture_id, current_user.id, db)
    op = db.query(models.FundingOpportunity).filter(models.FundingOpportunity.id == id).first()
    if not op:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Funding opportunity not found"}}
        )

    existing = db.query(models.FundingRequest).filter(
        models.FundingRequest.venture_id == venture.id,
        models.FundingRequest.funding_opportunity_id == op.id
    ).first()

    if existing:
        return FundingRequestResponse(
            id=existing.id,
            venture_id=existing.venture_id,
            funding_opportunity_id=existing.funding_opportunity_id,
            status=existing.status,
            created_at=existing.created_at
        )

    fr = models.FundingRequest(
        id=f"frq_{uuid.uuid4().hex[:12]}",
        venture_id=venture.id,
        funding_opportunity_id=op.id,
        status="requested"
    )
    db.add(fr)
    log_audit(
        db, actor_id=current_user.id, action="funding_requested",
        entity="funding_request", entity_id=fr.id,
        payload={"ventureId": venture.id, "opportunityId": op.id}
    )
    db.commit()
    db.refresh(fr)

    return FundingRequestResponse(
        id=fr.id,
        venture_id=fr.venture_id,
        funding_opportunity_id=fr.funding_opportunity_id,
        status=fr.status,
        created_at=fr.created_at
    )


# --- Financials, Transactions & Cap Table ---

@router.get("/ventures/{id}/financials", response_model=FinancialsOverviewResponse)
def get_venture_financials(
    id: str,
    range: str = Query("6m"),
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    snapshots = db.query(models.FinancialSnapshot).filter(
        models.FinancialSnapshot.venture_id == venture.id
    ).order_by(models.FinancialSnapshot.month.asc()).all()

    burn = 4500000
    rev = venture.mrr_cents or 4200000
    cash = 140200000
    if snapshots:
        latest = snapshots[-1]
        burn = latest.burn_cents
        rev = latest.revenue_cents
        cash = latest.cash_cents

    return FinancialsOverviewResponse(
        venture_id=venture.id,
        range=range,
        burn_cents=burn,
        monthly_burn_cents=burn,
        revenue_cents=rev,
        cash_cents=cash,
        runway_months=venture.runway_months,
        snapshots=[
            FinancialSnapshotResponse(
                id=s.id,
                venture_id=s.venture_id,
                month=s.month,
                burn_cents=s.burn_cents,
                revenue_cents=s.revenue_cents,
                cash_cents=s.cash_cents
            ) for s in snapshots
        ]
    )

@router.get("/ventures/{id}/transactions", response_model=ListResponse[TransactionResponse])
def get_venture_transactions(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    txs = db.query(models.Transaction).filter(
        models.Transaction.venture_id == venture.id
    ).order_by(models.Transaction.occurred_on.desc()).all()

    return ListResponse(
        items=[
            TransactionResponse(
                id=t.id,
                venture_id=t.venture_id,
                occurred_on=t.occurred_on,
                description=t.description,
                category=t.category,
                amount_cents=t.amount_cents,
                proof_hash=t.proof_hash,
                created_at=t.created_at
            ) for t in txs
        ],
        total=len(txs)
    )

@router.get("/ventures/{id}/cap-table", response_model=CapTableResponse)
def get_venture_cap_table(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    total = verify_cap_table_sum(venture.id, db)
    entries = db.query(models.CapTableEntry).filter(
        models.CapTableEntry.venture_id == venture.id
    ).all()

    return CapTableResponse(
        venture_id=venture.id,
        total_equity_pct=round(total, 4),
        total_equity=round(total, 4),
        entries=[
            CapTableEntryResponse(
                id=e.id,
                venture_id=e.venture_id,
                holder_user_id=e.holder_user_id,
                holder_label=e.holder_label,
                equity_pct=e.equity_pct,
                kind=e.kind,
                vested_pct=e.vested_pct
            ) for e in entries
        ]
    )

@router.get("/ventures/{id}/financials/export.csv")
def export_financials_csv(
    id: str,
    current_user: models.User = Depends(require_role("founder")),
    db: Session = Depends(get_db)
):
    venture = get_venture_for_founder(id, current_user.id, db)
    txs = db.query(models.Transaction).filter(
        models.Transaction.venture_id == venture.id
    ).order_by(models.Transaction.occurred_on.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Category", "Amount ($)", "Proof Hash"])
    for t in txs:
        amt_dollars = t.amount_cents / 100.0
        writer.writerow([t.occurred_on, t.description, t.category, f"{amt_dollars:.2f}", t.proof_hash])

    content = output.getvalue()
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={venture.name.lower().replace(' ', '_')}_financials.csv"}
    )
