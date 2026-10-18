from datetime import timedelta
from sqlalchemy.orm import Session
from database.models.investor import (
    InvestorProfile,
    Investment,
    MilestoneUpdate,
    MilestoneRead,
    DisclosureRequest,
)
from database.models.core import Notification, AuditLog
from .common import upsert, utcnow, canonical_hash
from .cast import (
    USR_FOUNDER_01,
    USR_INVESTOR_02,
    VEN_SYNTHETIX,
    VEN_POLYMATRIX,
    VEN_KAURI,
)

PHASE = 50

def run(db: Session):
    now = utcnow()

    # 1. Investor Profile
    upsert(
        db,
        InvestorProfile,
        {"user_id": USR_INVESTOR_02},
        {
            "tier": "Syndicate Tier 1",
            "wallet_address": "0x71C8821b0337E5652516A74C8215Ef72199B9901",
            "preferred_sectors": ["Enterprise AI", "Fintech Infrastructure", "Deep Tech", "Data Synthesis"],
            "instant_alerts": True,
            "weekly_digest": True,
            "accreditation_status": "verified",
            "accreditation_expires_at": now + timedelta(days=365),
            "created_at": now - timedelta(days=60),
            "updated_at": now - timedelta(days=60),
        },
    )

    # 2. Investments
    investments = [
        {
            "id": "invst_synth_01",
            "investor_id": USR_INVESTOR_02,
            "venture_id": VEN_SYNTHETIX,
            "instrument_type": "safe",
            "instrument_label": "Post-Money SAFE",
            "principal_cents": 20000000,    # $200,000
            "val_cap_cents": 1000000000,   # $10,000,000
            "discount_pct": 20.0,
            "equity_pct": 2.0,
            "contract_addr": "0x38F01b22992B45Ac01a88091bc88",
            "signed_on": now - timedelta(days=25),
            "status": "active",
        },
        {
            "id": "invst_poly_01",
            "investor_id": USR_INVESTOR_02,
            "venture_id": VEN_POLYMATRIX,
            "instrument_type": "safe",
            "instrument_label": "SAFE Note with MFN",
            "principal_cents": 15000000,    # $150,000
            "val_cap_cents": 800000000,    # $8,000,000
            "discount_pct": 20.0,
            "equity_pct": 1.875,
            "contract_addr": "0x49EA01771Ac01456bc99102844a",
            "signed_on": now - timedelta(days=20),
            "status": "active",
        },
        {
            "id": "invst_kauri_01",
            "investor_id": USR_INVESTOR_02,
            "venture_id": VEN_KAURI,
            "instrument_type": "grant",
            "instrument_label": "Grant & Warrant",
            "principal_cents": 7500000,     # $75,000
            "val_cap_cents": 500000000,    # $5,000,000
            "discount_pct": 15.0,
            "equity_pct": 1.5,
            "contract_addr": "0x12A09c550C881a2430bc990142b",
            "signed_on": now - timedelta(days=15),
            "status": "active",
        },
    ]

    for inv in investments:
        upsert(
            db,
            Investment,
            {"id": inv["id"]},
            {
                "investor_id": inv["investor_id"],
                "venture_id": inv["venture_id"],
                "instrument_type": inv["instrument_type"],
                "instrument_label": inv["instrument_label"],
                "principal_cents": inv["principal_cents"],
                "val_cap_cents": inv["val_cap_cents"],
                "discount_pct": inv["discount_pct"],
                "equity_pct": inv["equity_pct"],
                "contract_addr": inv["contract_addr"],
                "signed_on": inv["signed_on"],
                "status": inv["status"],
                "created_at": inv["signed_on"],
                "updated_at": inv["signed_on"],
            },
        )

    # 3. Milestone Updates
    mls_01 = upsert(
        db,
        MilestoneUpdate,
        {"id": "mls_synth_01"},
        {
            "venture_id": VEN_SYNTHETIX,
            "headline": "Sprint #3 Attested: 50,000 TPS MicroVM Stress Test Passed",
            "body": "Synthetix AI completed the autonomous agentic simulation pipeline benchmark. P99 latency measured at 1.42ms across all 48 test permutations with zero memory degradation.",
            "stage_label": "Phase 2 - Execution",
            "tag": "Engineering",
            "merkle_proof": canonical_hash({
                "sprint": "Sprint #3",
                "venture_id": VEN_SYNTHETIX,
                "tps": 50000,
                "p99_latency_ms": 1.42,
                "tests_passed": 48,
            }),
            "deliverables": ["Benchmark Suite", "Grafana Snapshot", "Attested Review Log"],
            "metrics": {"tps": 50000, "latencyP99Ms": 1.42, "testsPassed": 48},
            "published_at": now - timedelta(days=1),
            "created_at": now - timedelta(days=1),
        },
    )

    # 4. Milestone Reads (Composite PK)
    upsert(
        db,
        MilestoneRead,
        {"investor_id": USR_INVESTOR_02, "update_id": "mls_synth_01"},
        {"read_at": now - timedelta(hours=6)},
    )

    # 5. Disclosure Request
    upsert(
        db,
        DisclosureRequest,
        {"id": "dsc_synth_01"},
        {
            "investor_id": USR_INVESTOR_02,
            "venture_id": VEN_SYNTHETIX,
            "status": "approved",
            "created_at": now - timedelta(days=12),
            "updated_at": now - timedelta(days=12),
        },
    )

    # 6. Notifications
    notifications = [
        {
            "id": "notif_01",
            "user_id": USR_FOUNDER_01,
            "kind": "sprint_attestation",
            "body": "Candidate TX-5512B completed Sprint #3 with 96.4/100 score.",
            "read": False,
            "created_at": now - timedelta(hours=15),
        },
        {
            "id": "notif_03",
            "user_id": USR_INVESTOR_02,
            "kind": "milestone_published",
            "body": "Synthetix AI published Sprint #3 engineering milestone telemetry.",
            "read": True,
            "created_at": now - timedelta(hours=6),
        },
    ]

    for n in notifications:
        upsert(
            db,
            Notification,
            {"id": n["id"]},
            {
                "user_id": n["user_id"],
                "kind": n["kind"],
                "body": n["body"],
                "read": n["read"],
                "created_at": n["created_at"],
            },
        )

    # 7. Audit Log
    upsert(
        db,
        AuditLog,
        {"id": "aud_01"},
        {
            "actor_id": USR_FOUNDER_01,
            "action": "VENTURE_INITIALIZED",
            "entity": "ventures",
            "entity_id": VEN_SYNTHETIX,
            "payload": {"name": "Synthetix AI", "founder": USR_FOUNDER_01},
            "created_at": now - timedelta(days=60),
        },
    )
