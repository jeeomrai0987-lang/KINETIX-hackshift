from sqlalchemy.orm import Session
from database.models.core import User
from database.seed.common import hash_password
from database.seed.cast import (
    COHORT_ALPHA_ID, DEMO_PASSWORD,
    USR_WORKER_03, EMAIL_WORKER_03, CODE_ELENA,
    USR_WORKER_04, EMAIL_WORKER_04, CODE_JULIAN,
    USR_WORKER_05, EMAIL_WORKER_05, CODE_ROSTOVA,
)

USR_WORKER_EXTRA_1 = "usr_worker_extra_1"
EMAIL_WORKER_EXTRA_1 = "alex.chen@wasmstack.io"
CODE_EXTRA_1 = "TX-4401C"

USR_WORKER_EXTRA_2 = "usr_worker_extra_2"
EMAIL_WORKER_EXTRA_2 = "rachel.zhang@zerocopy.dev"
CODE_EXTRA_2 = "TX-3108D"

USR_WORKER_EXTRA_3 = "usr_worker_extra_3"
EMAIL_WORKER_EXTRA_3 = "david.kim@lowlatency.net"
CODE_EXTRA_3 = "TX-7720E"

PHASE = 10


def seed(db: Session):
    pwd_hash = hash_password(DEMO_PASSWORD)

    worker_users = [
        # 1. usr_worker_03: Elena Vance (TX-5512B)
        User(
            id=USR_WORKER_03,
            email=EMAIL_WORKER_03,
            password_hash=pwd_hash,
            name="Elena Vance",
            role="worker",
            title="High-Throughput Systems Engineer",
            avatar_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAXDAn8ZFbqaXgUtAZFPSAMimDjdAoYUtHj9L77g4tSh_dzBGXy6q7ARHBvvPaEiQBevjgoVWtUl1CPRgJcoZ_Gyr1x8Zo7gNTBlUQObPUZdavCilarTN6yVjeMbRs58962jPDHojUKOmZ_bPn3g6RPFzhAkTcS32gCbsLDrLoGoPt23xW2bo98EiFz6_G89_dt-TciA5PCjPGcobNbxFBrua1O80BXj8xC1JSaqoZGvJJLCVcC2Qyt0g",
            node_id=CODE_ELENA,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
        # 2. usr_worker_04: Julian Vance (TX-9042A)
        User(
            id=USR_WORKER_04,
            email=EMAIL_WORKER_04,
            password_hash=pwd_hash,
            name="Julian Vance",
            role="worker",
            title="Lead Distributed Systems Architect",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=256&q=80",
            node_id=CODE_JULIAN,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
        # 3. usr_worker_05: Elena Rostova (TX-8821B)
        User(
            id=USR_WORKER_05,
            email=EMAIL_WORKER_05,
            password_hash=pwd_hash,
            name="Elena Rostova",
            role="worker",
            title="Infrastructure Security & Sandbox Lead",
            avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=256&q=80",
            node_id=CODE_ROSTOVA,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
        # 4. usr_worker_extra_1: Alex Chen (TX-4401C)
        User(
            id=USR_WORKER_EXTRA_1,
            email=EMAIL_WORKER_EXTRA_1,
            password_hash=pwd_hash,
            name="Alex Chen",
            role="worker",
            title="Wasm Sandbox Infrastructure Lead",
            avatar_url="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=256&q=80",
            node_id=CODE_EXTRA_1,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
        # 5. usr_worker_extra_2: Rachel Zhang (TX-3108D)
        User(
            id=USR_WORKER_EXTRA_2,
            email=EMAIL_WORKER_EXTRA_2,
            password_hash=pwd_hash,
            name="Rachel Zhang",
            role="worker",
            title="Storage Engine Lead Architect",
            avatar_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=256&q=80",
            node_id=CODE_EXTRA_2,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
        # 6. usr_worker_extra_3: David Kim (TX-7720E)
        User(
            id=USR_WORKER_EXTRA_3,
            email=EMAIL_WORKER_EXTRA_3,
            password_hash=pwd_hash,
            name="David Kim",
            role="worker",
            title="Zero-Copy Network Systems Engineer",
            avatar_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=256&q=80",
            node_id=CODE_EXTRA_3,
            verified=True,
            cohort_id=COHORT_ALPHA_ID
        ),
    ]

    db.add_all(worker_users)
    db.flush()


def run(db: Session):
    seed(db)
