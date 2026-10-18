"""Seed founder financial data: cap table, restructuring events, transactions,
snapshots, funding opportunities, and funding requests (PHASE 40).

Strictly adheres to Contract Section 6 Rule 3 (Cap Table 100.0% integrity) and
reproduces the mock data from FounderStartup.jsx, FounderFinancial.jsx, and FounderFunding.jsx.
"""

from datetime import timedelta
from sqlalchemy.orm import Session
from database.models.finance import (
    CapTableEntry,
    RestructuringEvent,
    Transaction,
    FinancialSnapshot,
    FundingOpportunity,
    FundingRequest,
)
from .common import upsert, utcnow, canonical_hash
from .cast import (
    USR_FOUNDER_01,
    USR_COFOUNDER_01,
    USR_COFOUNDER_02,
    VEN_SYNTHETIX,
)

PHASE = 40


def run(db: Session):
    now = utcnow()

    # 1. Synthetix Cap Table (Summing exactly to 100.0%: 42.5 + 32.0 + 10.5 + 15.0 = 100.0%)
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

    # 2. Restructuring Events (as in FounderRestructuring.jsx)
    restructurings = [
        {
            "id": "rst_synth_01",
            "venture_id": VEN_SYNTHETIX,
            "type": "equity_reallocation",
            "from_user_id": None,  # From option pool / reserve
            "to_user_id": None,    # Staged for candidate TX-9042A
            "equity_delta_pct": 15.0,
            "stage": "Stage 04: Cap Table Re-Allocation",
            "note": "Succession pipeline REQ-SYNTH-8820B: Reallocating 15.0% founding reserve to Lead Distributed Systems Architect.",
            "executed_at": None,
            "created_at": now - timedelta(days=5),
        },
    ]

    for r in restructurings:
        upsert(
            db,
            RestructuringEvent,
            {"id": r["id"]},
            {
                "venture_id": r["venture_id"],
                "type": r["type"],
                "from_user_id": r["from_user_id"],
                "to_user_id": r["to_user_id"],
                "equity_delta_pct": r["equity_delta_pct"],
                "stage": r["stage"],
                "note": r["note"],
                "executed_at": r["executed_at"],
                "created_at": r["created_at"],
            },
        )

    # 3. Transactions with real SHA-256 proof_hash (as in FounderFinancial.jsx)
    txns = [
        {
            "id": "tx_101",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=4),
            "description": "AWS Cloud MicroVM GPU Cluster Soak Test",
            "category": "infrastructure",
            "amount_cents": -284000,  # -$2,840.00
            "payload": {"desc": "AWS Cloud MicroVM GPU Cluster Soak Test", "cents": -284000, "date": "2025-10-14"},
        },
        {
            "id": "tx_102",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=10),
            "description": "Enterprise Fintech Pilot Milestone Grant",
            "category": "revenue",
            "amount_cents": 1000000,  # +$10,000.00
            "payload": {"desc": "Enterprise Fintech Pilot Milestone Grant", "cents": 1000000, "date": "2025-10-08"},
        },
        {
            "id": "tx_103",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=18),
            "description": "Core Founding Squad Sprint #2 Stipends",
            "category": "payroll",
            "amount_cents": -950000,  # -$9,500.00
            "payload": {"desc": "Core Founding Squad Sprint #2 Stipends", "cents": -950000, "date": "2025-09-30"},
        },
        {
            "id": "tx_104",
            "venture_id": VEN_SYNTHETIX,
            "occurred_on": now - timedelta(days=33),
            "description": "Delaware C-Corp Legal & IP Assignment Filing",
            "category": "legal",
            "amount_cents": -145000,  # -$1,450.00
            "payload": {"desc": "Delaware C-Corp Legal & IP Assignment Filing", "cents": -145000, "date": "2025-09-15"},
        },
    ]

    for t in txns:
        proof = canonical_hash(t["payload"])  # Real 66-char SHA-256 with 0x prefix
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
                "proof_hash": proof,
                "created_at": t["occurred_on"],
            },
        )

    # 4. Financial Snapshots (6 months of monthly burn, revenue, cash)
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

    # 5. The Four Funding Opportunities (as in FounderFunding.jsx)
    opportunities = [
        {
            "id": "opp_1",
            "name": "Syndicate Alpha Angel Pool",
            "category": "syndicate",
            "check_min_cents": 25000000,  # $250,000
            "check_max_cents": 50000000,  # $500,000
            "structure": "Post-Money SAFE ($10M Cap, 20% Discount)",
            "tags": ["Enterprise AI", "Distributed Systems", "Lead Investor"],
            "timeline": "Terms Ready in 48 Hours",
            "base_fit_pct": 98.0,
        },
        {
            "id": "opp_2",
            "name": "Apex Horizon Capital",
            "category": "micro_vc",
            "check_min_cents": 40000000,  # $400,000
            "check_max_cents": 40000000,  # $400,000
            "structure": "Priced Seed / SAFE Side Letter",
            "tags": ["Fintech Infrastructure", "High Throughput"],
            "timeline": "Partner Review Scheduled",
            "base_fit_pct": 95.0,
        },
        {
            "id": "opp_3",
            "name": "NSF SBIR Phase I AI Grant",
            "category": "grant",
            "check_min_cents": 27500000,  # $275,000
            "check_max_cents": 27500000,  # $275,000
            "structure": "Non-Dilutive Federal Grant (0% Equity)",
            "tags": ["Zero Dilution", "Simulation Moat", "Government"],
            "timeline": "Submission Window Open",
            "base_fit_pct": 92.0,
        },
        {
            "id": "opp_4",
            "name": "Fintech Velocity Syndicate",
            "category": "syndicate",
            "check_min_cents": 15000000,  # $150,000
            "check_max_cents": 30000000,  # $300,000
            "structure": "SAFE Note with MFN & Pro-Rata",
            "tags": ["Banking Tech", "Agentic Workflows"],
            "timeline": "Attestation Room Verified",
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

    # 6. Active Funding Request
    upsert(
        db,
        FundingRequest,
        {"id": "fnr_01"},
        {
            "venture_id": VEN_SYNTHETIX,
            "funding_opportunity_id": "opp_1",
            "status": "submitted",
            "created_at": now - timedelta(days=15),
            "updated_at": now - timedelta(days=15),
        },
    )
