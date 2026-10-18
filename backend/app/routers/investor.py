import uuid
import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db import get_db, models
from backend.app.auth import require_role
from backend.app.schemas.base import ListResponse
from backend.app.schemas.auth import UserResponse
from backend.app.schemas.investor import (
    InvestorDashboardResponse, InvestmentDetailResponse, MilestoneUpdateResponse,
    InvestorSettingsUpdate, DisclosureRequestCreate, DisclosureRequestResponse
)
from backend.app.schemas.venture import VentureResponse
from backend.app.services.audit_service import log_audit

router = APIRouter(tags=["Investor"])

def user_to_response(u: Any) -> UserResponse:
    investor_p = None
    ip = getattr(u, "investor_profile", None)
    if ip:
        investor_p = {
            "tier": getattr(ip, "tier", None),
            "walletAddress": getattr(ip, "wallet_address", None),
            "preferredSectors": getattr(ip, "preferred_sectors", []) or [],
            "instantAlerts": getattr(ip, "instant_alerts", True),
            "weeklyDigest": getattr(ip, "weekly_digest", True),
            "accreditationStatus": getattr(ip, "accreditation_status", "verified"),
            "accreditationExpiresAt": getattr(ip, "accreditation_expires_at", None),
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
        investor_profile=investor_p,
        created_at=u.created_at
    )

@router.get("/investor/dashboard", response_model=InvestorDashboardResponse)
def get_investor_dashboard(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    investments = db.query(models.Investment).filter(
        models.Investment.investor_id == current_user.id
    ).all()

    total_capital = sum(i.principal_cents for i in investments)
    venture_ids = [i.venture_id for i in investments]

    # Milestone updates for ventures held
    updates = db.query(models.MilestoneUpdate).filter(
        models.MilestoneUpdate.venture_id.in_(venture_ids)
    ).all() if venture_ids else []

    read_update_ids = {
        r.update_id for r in db.query(models.MilestoneRead).filter(
            models.MilestoneRead.investor_id == current_user.id
        ).all()
    }

    unread_count = sum(1 for u in updates if u.id not in read_update_ids)

    holdings = []
    for inv in investments:
        v = inv.venture
        holdings.append({
            "id": inv.id,
            "ventureId": inv.venture_id,
            "ventureName": v.name if v else "Portfolio Co",
            "sector": v.sector if v else "AI",
            "principalCents": inv.principal_cents,
            "equityPct": inv.equity_pct,
            "valCapCents": inv.val_cap_cents,
            "stage": v.stage if v else "Sprint 3"
        })

    recent_milestones = []
    for u in updates[:5]:
        v = u.venture
        recent_milestones.append({
            "id": u.id,
            "headline": u.headline,
            "ventureName": v.name if v else "Venture",
            "stage": u.stage_label,
            "isRead": u.id in read_update_ids,
            "publishedAt": u.published_at.isoformat() if u.published_at else None
        })

    return InvestorDashboardResponse(
        user=user_to_response(current_user),
        capital_deployed_cents=total_capital,
        portfolio_count=len(investments),
        unread_updates_count=unread_count,
        holdings=holdings,
        recent_milestones=recent_milestones
    )

@router.get("/investor/portfolio", response_model=ListResponse[InvestmentDetailResponse])
def get_investor_portfolio(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    investments = db.query(models.Investment).filter(
        models.Investment.investor_id == current_user.id
    ).all()

    items = []
    for inv in investments:
        v = inv.venture
        items.append(InvestmentDetailResponse(
            id=inv.id,
            investor_id=inv.investor_id,
            venture_id=inv.venture_id,
            venture_name=v.name if v else "Venture",
            venture_sector=v.sector if v else "Autonomous Systems",
            venture_stage=v.stage if v else "Sprint 3",
            instrument_type=inv.instrument_type,
            instrument_label=inv.instrument_label,
            principal_cents=inv.principal_cents,
            val_cap_cents=inv.val_cap_cents,
            discount_pct=inv.discount_pct,
            equity_pct=inv.equity_pct,
            contract_addr=inv.contract_addr,
            signed_on=inv.signed_on,
            status=inv.status
        ))

    return ListResponse(items=items, total=len(items))

@router.get("/investor/updates", response_model=ListResponse[MilestoneUpdateResponse])
def get_investor_updates(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    investments = db.query(models.Investment).filter(
        models.Investment.investor_id == current_user.id
    ).all()
    venture_ids = [i.venture_id for i in investments]

    # Role isolation (Section 6 Rule 4):
    # Investors see updates of ventures they hold, or all cohort ventures if demo
    updates = db.query(models.MilestoneUpdate).filter(
        models.MilestoneUpdate.venture_id.in_(venture_ids)
    ).all() if venture_ids else []

    read_update_ids = {
        r.update_id for r in db.query(models.MilestoneRead).filter(
            models.MilestoneRead.investor_id == current_user.id
        ).all()
    }

    items = []
    for u in updates:
        v = u.venture
        items.append(MilestoneUpdateResponse(
            id=u.id,
            venture_id=u.venture_id,
            venture_name=v.name if v else "Venture",
            headline=u.headline,
            body=u.body,
            stage_label=u.stage_label,
            tag=u.tag,
            merkle_proof=u.merkle_proof,
            deliverables=u.deliverables or [],
            metrics=u.metrics or {},
            published_at=u.published_at,
            is_read=u.id in read_update_ids
        ))

    return ListResponse(items=items, total=len(items))

@router.post("/investor/updates/{id}/read")
def mark_update_as_read(
    id: str,
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    update = db.query(models.MilestoneUpdate).filter(models.MilestoneUpdate.id == id).first()
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Update not found"}}
        )

    read_entry = db.query(models.MilestoneRead).filter(
        models.MilestoneRead.investor_id == current_user.id,
        models.MilestoneRead.update_id == id
    ).first()

    if not read_entry:
        read_entry = models.MilestoneRead(
            investor_id=current_user.id,
            update_id=id,
            read_at=datetime.datetime.utcnow()
        )
        db.add(read_entry)
        db.commit()

    return {"message": "Update marked as read", "isRead": True}

@router.get("/investor/financial-reports")
def get_investor_financial_reports(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    investments = db.query(models.Investment).filter(
        models.Investment.investor_id == current_user.id
    ).all()

    reports = []
    for inv in investments:
        v = inv.venture
        if not v: continue
        snapshots = db.query(models.FinancialSnapshot).filter(
            models.FinancialSnapshot.venture_id == v.id
        ).order_by(models.FinancialSnapshot.month.desc()).limit(6).all()

        reports.append({
            "ventureId": v.id,
            "ventureName": v.name,
            "runwayMonths": v.runway_months,
            "mrrCents": v.mrr_cents,
            "raisedCents": v.raised_cents,
            "history": [
                {
                    "month": s.month,
                    "burnCents": s.burn_cents,
                    "revenueCents": s.revenue_cents,
                    "cashCents": s.cash_cents
                } for s in snapshots
            ]
        })

    return {"reports": reports}

@router.get("/investor/instruments")
def get_investor_instruments(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    investments = db.query(models.Investment).filter(
        models.Investment.investor_id == current_user.id
    ).all()

    return {
        "items": [
            {
                "id": inv.id,
                "ventureName": inv.venture.name if inv.venture else "Venture",
                "instrumentType": inv.instrument_type,
                "label": inv.instrument_label,
                "valCap": f"${inv.val_cap_cents / 100000000:.1f}M",
                "discount": f"{inv.discount_pct}%",
                "equity": f"{inv.equity_pct}%",
                "contractAddr": inv.contract_addr,
                "signedOn": inv.signed_on,
                "status": inv.status
            } for inv in investments
        ]
    }

@router.get("/investor/discover", response_model=ListResponse[VentureResponse])
def discover_cohort_startups(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    ventures = db.query(models.Venture).filter(models.Venture.status == "active").all()
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

@router.post("/investor/disclosure-requests", response_model=DisclosureRequestResponse)
def request_venture_disclosure(
    req: DisclosureRequestCreate,
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    venture = db.query(models.Venture).filter(models.Venture.id == req.venture_id).first()
    if not venture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "not_found", "message": "Venture not found"}}
        )

    existing = db.query(models.DisclosureRequest).filter(
        models.DisclosureRequest.investor_id == current_user.id,
        models.DisclosureRequest.venture_id == venture.id
    ).first()

    if existing:
        return DisclosureRequestResponse(
            id=existing.id,
            investor_id=existing.investor_id,
            venture_id=existing.venture_id,
            status=existing.status,
            created_at=existing.created_at
        )

    dr = models.DisclosureRequest(
        id=f"dsc_{uuid.uuid4().hex[:12]}",
        investor_id=current_user.id,
        venture_id=venture.id,
        status="pending"
    )
    db.add(dr)
    log_audit(
        db, actor_id=current_user.id, action="disclosure_requested",
        entity="disclosure_request", entity_id=dr.id,
        payload={"ventureId": venture.id}
    )
    db.commit()
    db.refresh(dr)

    return DisclosureRequestResponse(
        id=dr.id,
        investor_id=dr.investor_id,
        venture_id=dr.venture_id,
        status=dr.status,
        created_at=dr.created_at
    )

@router.get("/investor/settings")
def get_investor_settings(
    current_user: models.User = Depends(require_role("investor"))
):
    p = current_user.investor_profile
    return {
        "tier": p.tier if p else "Syndicate Tier 1",
        "walletAddress": p.wallet_address if p else "",
        "preferredSectors": p.preferred_sectors if p else [],
        "instantAlerts": p.instant_alerts if p else True,
        "weeklyDigest": p.weekly_digest if p else True,
        "accreditationStatus": p.accreditation_status if p else "verified",
        "accreditationExpiresAt": p.accreditation_expires_at.isoformat() if (p and p.accreditation_expires_at) else None
    }

@router.put("/investor/settings")
def update_investor_settings(
    req: InvestorSettingsUpdate,
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    p = current_user.investor_profile
    if not p:
        p = models.InvestorProfile(user_id=current_user.id)
        db.add(p)

    if req.tier is not None: p.tier = req.tier
    if req.wallet_address is not None: p.wallet_address = req.wallet_address
    if req.preferred_sectors is not None: p.preferred_sectors = req.preferred_sectors
    if req.instant_alerts is not None: p.instant_alerts = req.instant_alerts
    if req.weekly_digest is not None: p.weekly_digest = req.weekly_digest

    db.commit()
    return {
        "tier": p.tier,
        "walletAddress": p.wallet_address,
        "preferredSectors": p.preferred_sectors,
        "instantAlerts": p.instant_alerts,
        "weeklyDigest": p.weekly_digest,
        "accreditationStatus": p.accreditation_status,
        "accreditationExpiresAt": p.accreditation_expires_at.isoformat() if p.accreditation_expires_at else None
    }

@router.post("/investor/settings/recertify")
def recertify_accreditation(
    current_user: models.User = Depends(require_role("investor")),
    db: Session = Depends(get_db)
):
    p = current_user.investor_profile
    if not p:
        p = models.InvestorProfile(user_id=current_user.id)
        db.add(p)

    p.accreditation_status = "verified"
    p.accreditation_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=365)
    log_audit(db, actor_id=current_user.id, action="investor_recertified", entity="user", entity_id=current_user.id)
    db.commit()

    return {
        "message": "SEC Rule 506(c) Accreditation recertified successfully for 365 days.",
        "accreditationStatus": p.accreditation_status,
        "accreditationExpiresAt": p.accreditation_expires_at.isoformat()
    }
