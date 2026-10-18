from datetime import timedelta
from sqlalchemy.orm import Session
from database.models.finance import (
    CapTableEntry,
    Transaction,
    FinancialSnapshot,
    FundingOpportunity,
    FundingRequest,
)
from .common import upsert, utcnow
from .cast import (
    USR_FOUNDER_01,
    USR_COFOUNDER_01,
    USR_COFOUNDER_02,
    VEN_SYNTHETIX,
)

PHASE = 40

def run(db: Session):
    now = utcnow()

    # 1. Cap Table (Section 6 Rule 3: 42.5 + 32.0 + 10.5 + 15.0 = 100.0%)
    cap_entries = [
        {
            "id": "cap_synth_01",
            "venture_id": VEN_SYNTHETIX,
            "holder_user_id": USR_FOUNDER_01,
            "holder_label": "Alex Mercer (CEO)",
            "equity_pct": 42.5,
            "kind": "founder",
            "vested_pct": 25.0,
            "created_at": now - timedelta(days=60),
        },
        {
            "id": "cap_synth_02",
            "venture_id": VEN_SYNTHETIX,
            "holder_user_id": USR_COFOUNDER_01,
            "holder_label": "Marcus Chen (CTO)",
            "equity_pct": 32.0,
            "kind": "cofounder",
            "vested_pct": 20.0,
            "created_at": now - timedelta(days=60),
        },
        {
            "id": "cap_synth_03",
            "venture_id": VEN_SYNTHETIX,
            "holder_user_id": USR_COFOUNDER_02,
            "holder_label": "Sarah Jenkins (Growth)",
            "equity_pct": 10.5,
            "kind": "cofounder",
            "vested_pct": 15.0,
            "created_at": now - timedelta(days=60),
        },
        {
            "id": "cap_synth_04",
            "venture_id": VEN_SYNTHETIX,
            "holder_user_id": None,
            "holder_label": "Open Founding Reserve / Option Pool",
            "equity_pct": 15.0,
            "kind": "option_pool",
            "vested_pct": 0.0,
            "created_at": now - timedelta(days=60),
        },
    ]

    for cap in cap_entries:
        upsert(
            db,
            CapTableEntry,
            {"id": cap["id"]},
            {
                "venture_id": cap["venture_id"],
                "holder_user_id": cap["holder_user_id"],
                "holder_label": cap["holder_label"],
                "equity_pct": cap["equity_pct"],
                "kind": cap["kind"],
                "vested_pct": cap["vested_pct"],
                "created_at": cap["created_at"],
                "updated_at": cap["created_at"],
            },
        )

    # 2. Transactions (PHASE 50)
    txns = [
        {
            "id": "txn_101",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=4),
            "description": "AWS Cloud MicroVM GPU Cluster Soak Test",
            "category": "infrastructure",
            "amount_cents": -284000,  # -$2,840.00
            "proof_hash": "0x8f9c21aa54b8e991204cf01284a1801c890123ef",
        },
        {
            "id": "txn_102",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=10),
            "description": "Enterprise Fintech Pilot Milestone Grant",
            "category": "revenue",
            "amount_cents": 1000000,  # +$10,000.00
            "proof_hash": "0x3f7a8849921bcdef0123456789abcdef01234567",
        },
        {
            "id": "txn_103",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=18),
            "description": "Core Founding Squad Sprint #2 Stipends",
            "category": "payroll",
            "amount_cents": -950000,  # -$9,500.00
            "proof_hash": "0x12bb774088ac890123456789abcdef0123456789",
        },
        {
            "id": "txn_104",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=33),
            "description": "Delaware C-Corp Legal & IP Assignment Filing",
            "category": "legal",
            "amount_cents": -145000,  # -$1,450.00
            "proof_hash": "0x7e29bb10cc40890123456789abcdef0123456789",
        },
    ]

    for t in txns:
        upsert(
            db,
            Transaction,
            {"id": t["id"]},
            {
                "venture_id": t["venture_id"],
                "occurred_on": t["occurred_on"],
                "description": t["description"],
                "category": t["category"],
                "amount_cents": t["amount_cents"],
                "proof_hash": t["proof_hash"],
                "created_at": t["occurred_on"],
            },
        )

    # 3. Financial Snapshots (6 months)
    snapshots = [
        ("2025-05", 1200000, 300000, 29000000),
        ("2025-06", 1320000, 450000, 28130000),
        ("2025-07", 1400000, 550000, 27280000),
        ("2025-08", 1450000, 680000, 26510000),
        ("2025-09", 1480000, 750000, 25780000),
        ("2025-10", 1480000, 850000, 24250000),
    ]

    for idx, (m, burn, rev, cash) in enumerate(snapshots):
        upsert(
            db,
            FinancialSnapshot,
            {"id": f"snp_synth_{idx+1}"},
            {
                "venture_id": VEN_SYNTHETIX,
                "month": m,
                "burn_cents": burn,
                "revenue_cents": rev,
                "cash_cents": cash,
                "created_at": now - timedelta(days=(6 - idx) * 30),
            },
        )

    # 4. Funding Opportunities
    opportunities = [
        {
            "id": "opp_01",
            "name": "Fintech Infrastructure Angel Syndicate",
            "category": "syndicate",
            "check_min_cents": 5000000,   # $50k
            "check_max_cents": 25000000,  # $250k
            "structure": "Post-Money SAFE",
            "tags": ["Enterprise AI", "Fintech Infrastructure", "MicroVM"],
            "timeline": "2 Weeks",
            "base_fit_pct": 94.0,
        },
        {
            "id": "opp_02",
            "name": "Deep Tech Velocity Micro-VC",
            "category": "micro_vc",
            "check_min_cents": 20000000,  # $200k
            "check_max_cents": 50000000,  # $500k
            "structure": "Priced Seed",
            "tags": ["AI Core", "Infrastructure", "High-Throughput"],
            "timeline": "4 Weeks",
            "base_fit_pct": 88.5,
        },
        {
            "id": "opp_03",
            "name": "NSF Agentic Safety Research Grant",
            "category": "grant",
            "check_min_cents": 7500000,   # $75k
            "check_max_cents": 15000000,  # $150k
            "structure": "Non-Dilutive Grant",
            "tags": ["Safety", "Compliance", "Deterministic"],
            "timeline": "Immediate",
            "base_fit_pct": 91.0,
        },
    ]

    for opp in opportunities:
        upsert(
            db,
            FundingOpportunity,
            {"id": opp["id"]},
            {
                "name": opp["name"],
                "category": opp["category"],
                "check_min_cents": opp["check_min_cents"],
                "check_max_cents": opp["check_max_cents"],
                "structure": opp["structure"],
                "tags": opp["tags"],
                "timeline": opp["timeline"],
                "base_fit_pct": opp["base_fit_pct"],
                "created_at": now - timedelta(days=20),
            },
        )

    # 5. Funding Request
    upsert(
        db,
        FundingRequest,
        {"id": "fnr_01"},
        {
            "venture_id": VEN_SYNTHETIX,
            "funding_opportunity_id": "opp_01",
            "status": "approved",
            "created_at": now - timedelta(days=15),
            "updated_at": now - timedelta(days=15),
        },
    )
