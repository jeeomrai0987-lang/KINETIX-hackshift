"""Seed Arena candidate matches for Synthetix AI (PHASE 40).

Respects Contract Section 6 Rule 1 (Blind Protocol) and Section 7 Demo Cast.
Worker rows come from Person B's PHASE 10 (do not create workers yourself).
"""

from datetime import timedelta
from sqlalchemy.orm import Session
from database.models.core import User
from database.models.venture import Match, SquadRole
from .common import upsert, utcnow
from .cast import (
    VEN_SYNTHETIX,
    USR_WORKER_03,
    USR_WORKER_04,
    USR_WORKER_05,
    CODE_JULIAN,
    CODE_ELENA,
    CODE_ROSTOVA,
)

PHASE = 40


def run(db: Session):
    now = utcnow()
    role_id = "rol_synth_04"

    # Verify role exists
    role = db.get(SquadRole, role_id)
    if not role:
        return

    matches = [
        {
            "id": "mat_synth_01",
            "venture_id": VEN_SYNTHETIX,
            "role_id": role_id,
            "worker_id": USR_WORKER_04,
            "candidate_code": CODE_JULIAN,  # TX-9042A
            "synergy_score": 96.0,
            "fit_details": {
                "fitDetails": "Perfect cognitive counterbalance to CTO Marcus Chen. Outstanding low-level networking velocity.",
                "skills": ["Distributed Systems", "Rust", "Raft Consensus", "Kubernetes Operator", "MicroVM"],
                "experience": "8+ Years Verifiable Production",
            },
            "status": "suggested",
        },
        {
            "id": "mat_synth_02",
            "venture_id": VEN_SYNTHETIX,
            "role_id": role_id,
            "worker_id": USR_WORKER_03,
            "candidate_code": CODE_ELENA,  # TX-5512B
            "synergy_score": 94.0,
            "fit_details": {
                "fitDetails": "High execution consistency in latency stress trials. Zero critical knowledge gaps identified.",
                "skills": ["Go", "Distributed State", "gRPC", "Zero-Copy IO", "Fintech Protocols"],
                "experience": "6 Years Production Systems",
            },
            "status": "suggested",
        },
        {
            "id": "mat_synth_03",
            "venture_id": VEN_SYNTHETIX,
            "role_id": role_id,
            "worker_id": USR_WORKER_05,
            "candidate_code": CODE_ROSTOVA,  # TX-8821B
            "synergy_score": 91.0,
            "fit_details": {
                "fitDetails": "Specialized in adversarial simulation resilience and zero-knowledge telemetry pipes.",
                "skills": ["Wasm Runtime", "Sandbox Isolation", "eBPF", "C/C++", "Audit Attestation"],
                "experience": "7 Years Deep Tech",
            },
            "status": "suggested",
        },
    ]

    for m in matches:
        # Worker rows come from Person B's PHASE 10; do not create workers yourself
        worker_user = db.get(User, m["worker_id"])
        if not worker_user:
            # Person B's Phase 10 has not run yet in this environment
            continue

        upsert(
            db,
            Match,
            {"id": m["id"]},
            {
                "venture_id": m["venture_id"],
                "role_id": m["role_id"],
                "worker_id": m["worker_id"],
                "candidate_code": m["candidate_code"],
                "synergy_score": m["synergy_score"],
                "fit_details": m["fit_details"],
                "status": m["status"],
                "created_at": now - timedelta(days=2),
                "updated_at": now - timedelta(days=2),
            },
        )
