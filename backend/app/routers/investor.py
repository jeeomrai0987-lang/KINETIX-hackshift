import uuid
import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import (
    User, InvestorProfile, Investment, MilestoneUpdate, MilestoneRead,
    DisclosureRequest, Venture, FinancialSnapshot, AuditLog
)
from backend.app.auth import require_role
from backend.app.schemas.investor import (
    InvestorSettingsUpdate, DisclosureRequestCreate
)

router = APIRouter(tags=["investor"])


@router.get("/investor/dashboard")
def get_investor_dashboard(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    investments = db.query(Investment).filter(Investment.investor_id == user.id).all()
    v_ids = [inv.venture_id for inv in investments]

    # Unread updates
    updates = db.query(MilestoneUpdate).filter(MilestoneUpdate.venture_id.in_(v_ids)).all() if v_ids else []
    read_ids = {
        mr.update_id for mr in db.query(MilestoneRead).filter(MilestoneRead.investor_id == user.id).all()
    }
    unread_count = len([u for u in updates if u.id not in read_ids])

    total_committed_cents = sum(inv.principal_cents for inv in investments)

    return {
        "portfolioCount": len(investments),
        "totalCommittedCents": total_committed_cents,
        "unreadMilestonesCount": unread_count,
        "disclosureRequestsCount": db.query(DisclosureRequest).filter(DisclosureRequest.investor_id == user.id).count(),
        "disclaimer": "Illustrative calculations only. Returns are not guaranteed. No equity or securities are bought or sold.",
        "recentUpdates": [
            {
                "id": u.id,
                "ventureName": u.venture.name if u.venture else "Venture",
                "headline": u.headline,
                "stage": u.stage_label,
                "isRead": u.id in read_ids,
                "publishedAt": u.published_at.strftime("%b %d, %Y") if u.published_at else ""
            } for u in updates[:4]
        ]
    }


@router.get("/investor/portfolio")
def get_investor_portfolio(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    investments = db.query(Investment).filter(Investment.investor_id == user.id).all()
    items = []
    for inv in investments:
        v = inv.venture
        items.append({
            "id": inv.id,
            "ventureId": inv.venture_id,
            "name": v.name if v else "Venture",
            "stage": v.stage if v else "Seed Stage",
            "instrument": inv.instrument_label,
            "principal": f"${inv.principal_cents // 100:,}",
            "principalCents": inv.principal_cents,
            "valCap": f"${inv.val_cap_cents // 100:,}",
            "discount": f"{inv.discount_pct}%",
            "equityPct": f"{inv.equity_pct}%",
            "runway": f"{v.runway_months} Months" if v else "12.0 Months",
            "mrr": f"${v.mrr_cents // 100:,}" if v else "$0",
            "score": f"{v.clarity_score}/100" if v else "90/100",
            "founder": f"{v.founder.name} (CEO)" if v and v.founder else "Founder",
            "thesis": v.thesis if v else "",
            "tags": [v.sector] if v else ["AI"],
            "contractAddr": inv.contract_addr
        })
    return {"items": items, "total": len(items)}


@router.get("/investor/updates")
def get_investor_updates(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    # Only ventures investor holds stakes in
    investments = db.query(Investment).filter(Investment.investor_id == user.id).all()
    v_ids = [inv.venture_id for inv in investments]

    if not v_ids:
        return {"items": [], "total": 0}

    updates = db.query(MilestoneUpdate).filter(MilestoneUpdate.venture_id.in_(v_ids)).order_by(MilestoneUpdate.published_at.desc()).all()
    read_ids = {
        mr.update_id for mr in db.query(MilestoneRead).filter(MilestoneRead.investor_id == user.id).all()
    }

    items = []
    for u in updates:
        items.append({
            "id": u.id,
            "ventureId": u.venture_id,
            "ventureName": u.venture.name if u.venture else "Venture",
            "headline": u.headline,
            "body": u.body,
            "stage": u.stage_label,
            "tag": u.tag,
            "merkleProof": u.merkle_proof,
            "deliverables": u.deliverables,
            "metrics": u.metrics,
            "isRead": u.id in read_ids,
            "publishedAt": u.published_at.strftime("%b %d, %Y") if u.published_at else ""
        })
    return {"items": items, "total": len(items)}


@router.post("/investor/updates/{id}/read")
def mark_update_read(
    id: str,
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    mr = db.query(MilestoneRead).filter(
        MilestoneRead.investor_id == user.id,
        MilestoneRead.update_id == id
    ).first()
    if not mr:
        mr = MilestoneRead(investor_id=user.id, update_id=id)
        db.add(mr)
        db.commit()
    return {"status": "success", "isRead": True}


@router.get("/investor/financial-reports")
def get_investor_financial_reports(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    investments = db.query(Investment).filter(Investment.investor_id == user.id).all()
    v_ids = [inv.venture_id for inv in investments]

    snaps = db.query(FinancialSnapshot).filter(FinancialSnapshot.venture_id.in_(v_ids)).order_by(FinancialSnapshot.month.asc()).all() if v_ids else []

    latest = snaps[-1] if snaps else None

    return {
        "monthlyBurn": f"-${latest.burn_cents // 100:,}" if latest else "-$14,800",
        "treasuryBalance": f"${latest.cash_cents // 100:,}" if latest else "$242,500",
        "netRunway": "16.4 Mos",
        "regulatoryNote": "Simulated financial telemetry. Past performance is no guarantee of future returns.",
        "snapshots": [
            {
                "month": s.month,
                "burn": f"-${s.burn_cents // 100:,}",
                "revenue": f"+${s.revenue_cents // 100:,}",
                "cash": f"${s.cash_cents // 100:,}"
            } for s in snaps
        ]
    }


@router.get("/investor/instruments")
def get_investor_instruments(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    investments = db.query(Investment).filter(Investment.investor_id == user.id).all()
    items = []
    for inv in investments:
        items.append({
            "id": inv.id,
            "ventureName": inv.venture.name if inv.venture else "Venture",
            "instrumentType": inv.instrument_type,
            "instrumentLabel": inv.instrument_label,
            "principalCents": inv.principal_cents,
            "valCapCents": inv.val_cap_cents,
            "discountPct": inv.discount_pct,
            "equityPct": inv.equity_pct,
            "contractAddr": inv.contract_addr,
            "signedOn": inv.signed_on.strftime("%b %d, %Y") if inv.signed_on else "",
            "status": inv.status
        })
    return {"items": items, "total": len(items)}


@router.get("/investor/discover")
def get_discover_startups(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    # Discovery list of cohort ventures
    ventures = db.query(Venture).all()
    items = []
    for v in ventures:
        items.append({
            "id": v.id,
            "name": v.name,
            "sector": v.sector,
            "stage": v.stage,
            "clarityScore": v.clarity_score,
            "thesis": v.thesis,
            "founderName": v.founder.name if v.founder else "Founder",
            "raised": f"${v.raised_cents // 100:,}",
            "verifiedSprintScore": "94.2 / 100"
        })
    return {"items": items, "total": len(items)}


@router.post("/investor/disclosure-requests")
def create_disclosure_request(
    req: DisclosureRequestCreate,
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    v = db.query(Venture).filter(Venture.id == req.venture_id).first()
    if not v:
        raise HTTPException(status_code=404, detail={"error": {"code": "VENTURE_NOT_FOUND", "message": "Venture not found"}})

    dr = DisclosureRequest(
        id=f"dr_{uuid.uuid4().hex[:12]}",
        investor_id=user.id,
        venture_id=v.id,
        status="pending"
    )
    db.add(dr)

    db.add(AuditLog(
        id=f"aud_{uuid.uuid4().hex[:12]}",
        actor_id=user.id,
        action="disclosure_requested",
        entity="disclosure_request",
        entity_id=dr.id,
        payload={"venture": v.name}
    ))
    db.commit()

    return {"status": "success", "message": f"Disclosure request submitted to {v.name}"}


@router.get("/investor/settings")
def get_investor_settings(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    prof = db.query(InvestorProfile).filter(InvestorProfile.user_id == user.id).first()
    return {
        "tier": prof.tier if prof else "Syndicate Member",
        "walletAddress": prof.wallet_address if prof else "",
        "preferredSectors": prof.preferred_sectors if prof else [],
        "instantAlerts": prof.instant_alerts if prof else True,
        "weeklyDigest": prof.weekly_digest if prof else True,
        "accreditationStatus": prof.accreditation_status if prof else "verified",
        "accreditationExpiresAt": prof.accreditation_expires_at.strftime("%b %d, %Y") if prof and prof.accreditation_expires_at else "Dec 31, 2026"
    }


@router.put("/investor/settings")
def update_investor_settings(
    req: InvestorSettingsUpdate,
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    prof = db.query(InvestorProfile).filter(InvestorProfile.user_id == user.id).first()
    if prof:
        if req.preferred_sectors is not None: prof.preferred_sectors = req.preferred_sectors
        if req.wallet_address is not None: prof.wallet_address = req.wallet_address
        if req.instant_alerts is not None: prof.instant_alerts = req.instant_alerts
        if req.weekly_digest is not None: prof.weekly_digest = req.weekly_digest
        db.commit()
    return {"status": "success", "message": "Investor settings updated"}


@router.post("/investor/settings/recertify")
def recertify_investor(
    user: User = Depends(require_role(["investor"])),
    db: Session = Depends(get_db)
):
    prof = db.query(InvestorProfile).filter(InvestorProfile.user_id == user.id).first()
    if prof:
        prof.accreditation_status = "verified"
        prof.accreditation_expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
        db.commit()
    return {"status": "success", "accreditationStatus": "verified", "message": "Accreditation re-certified for 12 months"}
