from datetime import timedelta
from sqlalchemy.orm import Session
from database.models.core import Cohort, User
from .common import hash_password, upsert, utcnow
from .cast import (
    COHORT_ALPHA_ID,
    COHORT_ALPHA_NAME,
    COHORT_ALPHA_BATCH,
    USR_FOUNDER_01,
    USR_COFOUNDER_01,
    USR_COFOUNDER_02,
    USR_INVESTOR_02,
    USR_FOUNDER_POLY,
    USR_FOUNDER_CHRONO,
    USR_FOUNDER_KAURI,
    USR_FOUNDER_AETHER,
    EMAIL_FOUNDER_01,
    EMAIL_COFOUNDER_01,
    EMAIL_COFOUNDER_02,
    EMAIL_INVESTOR_02,
    NODE_FOUNDER_01,
    NODE_COFOUNDER_01,
    NODE_COFOUNDER_02,
    NODE_INVESTOR_02,
)

PHASE = 10

def run(db: Session):
    now = utcnow()
    pwd_hash = hash_password("Demo#2026")

    # 1. Cohort
    upsert(
        db,
        Cohort,
        {"id": COHORT_ALPHA_ID},
        {
            "name": COHORT_ALPHA_NAME,
            "batch_no": COHORT_ALPHA_BATCH,
            "created_at": now - timedelta(days=90),
        },
    )

    # 2. Founder Users
    founders = [
        {
            "id": USR_FOUNDER_01,
            "email": EMAIL_FOUNDER_01,
            "name": "Alex Mercer",
            "role": "founder",
            "title": "Founder & CEO",
            "avatar_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCrFd9FXpH1DVp90x6QYI3kcBlABNYtgFYxaa-elUwjSWxyV56HX1Uir3Bo-JqKk3TkfehwV64tbjsMvhw9FVCYgdY2H_bGj_WUycEQb8Dik8Hw6UG-DAyLKzDMeTucfRCt_DgSFD6L_pCOl0A8YFS_ujCydDFtmuuoeY7hOIu_gb7QgAuFUQWPIUNLCYl78krYPxXqb-rVILLe9UGsKUdf2HDshK8T-ZrUTNmAMRphT1t5VEKD26jNtQ",
            "node_id": NODE_FOUNDER_01,
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_COFOUNDER_01,
            "email": EMAIL_COFOUNDER_01,
            "name": "Marcus Chen",
            "role": "founder",
            "title": "Co-Founder & CTO",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=256&q=80",
            "node_id": NODE_COFOUNDER_01,
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_COFOUNDER_02,
            "email": EMAIL_COFOUNDER_02,
            "name": "Sarah Jenkins",
            "role": "founder",
            "title": "Head of Enterprise Growth",
            "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=256&q=80",
            "node_id": NODE_COFOUNDER_02,
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_FOUNDER_POLY,
            "email": "aaron.meyer@polymatrix.ai",
            "name": "Dr. Aaron Meyer",
            "role": "founder",
            "title": "Founder & CEO",
            "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=256&q=80",
            "node_id": "NODE-FND-0004",
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_FOUNDER_CHRONO,
            "email": "vikram.joshi@chronodb.io",
            "name": "Vikram Joshi",
            "role": "founder",
            "title": "Founder & CEO",
            "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=256&q=80",
            "node_id": "NODE-FND-0005",
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_FOUNDER_KAURI,
            "email": "maya.lin@kaurihealth.org",
            "name": "Dr. Maya Lin",
            "role": "founder",
            "title": "Founder & CEO",
            "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=256&q=80",
            "node_id": "NODE-FND-0006",
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_FOUNDER_AETHER,
            "email": "liam.thorne@aetherlabs.xyz",
            "name": "Liam Thorne",
            "role": "founder",
            "title": "Founder & CEO",
            "avatar_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=256&q=80",
            "node_id": "NODE-FND-0007",
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
        {
            "id": USR_INVESTOR_02,
            "email": EMAIL_INVESTOR_02,
            "name": "Marcus Vance",
            "role": "investor",
            "title": "Investor / Angel Syndicate Partner",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80",
            "node_id": NODE_INVESTOR_02,
            "verified": True,
            "cohort_id": COHORT_ALPHA_ID,
        },
    ]

    for f in founders:
        upsert(
            db,
            User,
            {"id": f["id"]},
            {
                "email": f["email"],
                "password_hash": pwd_hash,
                "name": f["name"],
                "role": f["role"],
                "title": f["title"],
                "avatar_url": f["avatar_url"],
                "node_id": f["node_id"],
                "verified": f["verified"],
                "cohort_id": f["cohort_id"],
                "created_at": now - timedelta(days=60),
                "updated_at": now - timedelta(days=60),
            },
        )
