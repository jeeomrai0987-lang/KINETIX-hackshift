import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from database.models.worker_activity import Invitation, Submission, Application, ProofReport
from database.seed.common import canonical_hash
from database.seed.cast import (
    VEN_SYNTHETIX, VEN_POLYMATRIX, VEN_CHRONODB,
    USR_WORKER_03, USR_WORKER_04, USR_WORKER_05,
    CODE_ELENA, CODE_JULIAN, CODE_ROSTOVA
)
from database.seed.seed_worker_people import USR_WORKER_EXTRA_1

PHASE = 40


def get_submission_payload(sub: Submission) -> Dict[str, Any]:
    """Generates the canonical scored payload dictionary for a challenge submission."""
    return {
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


def get_proof_report_payload(report: ProofReport) -> Dict[str, Any]:
    """Generates the canonical payload dictionary for an attested proof of work report."""
    return {
        "cohort_rank": report.cohort_rank,
        "id": report.id,
        "memory_leak_bytes": report.memory_leak_bytes,
        "p99_latency_ms": report.p99_latency_ms,
        "reviewer_verdict": report.reviewer_verdict,
        "score": report.score,
        "sprint_name": report.sprint_name,
        "submission_id": report.submission_id,
        "tests_passed": report.tests_passed,
        "tests_total": report.tests_total,
        "worker_id": report.worker_id,
    }


def seed_relations(db: Session):
    """PHASE 40: Seed invitations, applications, and submissions."""
    now = datetime.datetime.now(datetime.timezone.utc)

    # 1. Three pending invitations from WorkerInvitations.jsx (equity as numeric float percents)
    invitations = [
        Invitation(
            id="inv_1",
            venture_id=VEN_SYNTHETIX,
            role_id="rol_synth_04",
            worker_id=USR_WORKER_03,
            equity_pct=15.0,
            terms="4-Year Vesting with 1-Year Cliff • Post-Money SAFE Protected",
            message="We reviewed your 50k TPS MicroVM benchmark submission and were blown away by your low-latency scheduler execution. We would love to have you as a founding team member to build out our high-throughput enterprise simulation stack.",
            status="pending",
            responded_at=None
        ),
        Invitation(
            id="inv_2",
            venture_id=VEN_POLYMATRIX,
            role_id="rol_poly_01",
            worker_id=USR_WORKER_03,
            equity_pct=12.0,
            terms="Standard Founder Stock Agreement • Early Exercise Supported",
            message="Your background in distributed state synchronization fits perfectly with our continuous compliance simulation architecture.",
            status="pending",
            responded_at=None
        ),
        Invitation(
            id="inv_3",
            venture_id=VEN_CHRONODB,
            role_id="rol_chrono_01",
            worker_id=USR_WORKER_03,
            equity_pct=14.0,
            terms="Delaware C-Corp Cap Table Slot • Series Pre-Seed",
            message="We are building the fastest vector storage engine for LLMs. Your zero-copy memory benchmarks match our exact technical roadmap requirements.",
            status="pending",
            responded_at=None
        ),
    ]
    db.add_all(invitations)

    # 2. Applications with blind_token
    applications = [
        Application(
            id="app_1",
            role_id="rol_aether_01",
            worker_id=USR_WORKER_05,
            blind_token="BLIND-TOK-8821B",
            status="submitted"
        ),
        Application(
            id="app_2",
            role_id="rol_poly_01",
            worker_id=USR_WORKER_EXTRA_1,
            blind_token="BLIND-TOK-4401C",
            status="submitted"
        ),
    ]
    db.add_all(applications)

    # 3. Three challenge submissions with vector scores from FounderChallenge.jsx
    sub_01 = Submission(
        id="sub_01",
        challenge_id="chl_synth_01",
        worker_id=USR_WORKER_04,
        candidate_code=f"Candidate #{CODE_JULIAN}",
        status="attested",
        score=94.2,
        p99_latency_ms=3.8,
        tests_passed=50000,
        tests_total=50000,
        replay_integrity=98.0,
        failure_recovery=95.0,
        concurrency_latency=92.0,
        code_elegance=91.0,
        reviewer_verdict="3/3 Unanimous Blind Pass",
        signed_at=now - datetime.timedelta(hours=12),
        hash=""  # will be computed below
    )
    sub_01.hash = canonical_hash(get_submission_payload(sub_01))

    sub_02 = Submission(
        id="sub_02",
        challenge_id="chl_synth_01",
        worker_id=USR_WORKER_03,
        candidate_code=f"Candidate #{CODE_ELENA}",
        status="attested",
        score=88.5,
        p99_latency_ms=4.6,
        tests_passed=49812,
        tests_total=50000,
        replay_integrity=90.0,
        failure_recovery=88.0,
        concurrency_latency=89.0,
        code_elegance=87.0,
        reviewer_verdict="3/3 Unanimous Blind Pass",
        signed_at=now - datetime.timedelta(hours=6),
        hash=""  # will be computed below
    )
    sub_02.hash = canonical_hash(get_submission_payload(sub_02))

    sub_03 = Submission(
        id="sub_03",
        challenge_id="chl_synth_01",
        worker_id=USR_WORKER_05,
        candidate_code=f"Candidate #{CODE_ROSTOVA}",
        status="in_review",
        score=84.0,
        p99_latency_ms=5.1,
        tests_passed=48900,
        tests_total=50000,
        replay_integrity=86.0,
        failure_recovery=84.0,
        concurrency_latency=82.0,
        code_elegance=84.0,
        reviewer_verdict="Scoring In Review",
        signed_at=None,
        hash=""  # will be computed below
    )
    sub_03.hash = canonical_hash(get_submission_payload(sub_03))

    db.add_all([sub_01, sub_02, sub_03])
    db.flush()


def seed_proof_reports(db: Session):
    """PHASE 50: Seed proof reports from WorkerProofOfWork.jsx with verifiable canonical hashes."""
    now = datetime.datetime.now(datetime.timezone.utc)

    pr_1 = ProofReport(
        id="pr_1",
        worker_id=USR_WORKER_03,
        submission_id="sub_02",
        sprint_name="Sprint #3: MicroVM Concurrency & Adversarial Simulation",
        completed_at=now - datetime.timedelta(days=2),
        score=96.4,
        cohort_rank=2,
        tests_passed=50000,
        tests_total=50000,
        p99_latency_ms=3.8,
        memory_leak_bytes=0,
        reviewer_verdict="3/3 Unanimous Blind Pass",
        hash=""
    )
    pr_1.hash = canonical_hash(get_proof_report_payload(pr_1))

    pr_2 = ProofReport(
        id="pr_2",
        worker_id=USR_WORKER_03,
        submission_id=None,
        sprint_name="Sprint #2: Distributed Consensus & Partition Healing",
        completed_at=now - datetime.timedelta(days=16),
        score=94.0,
        cohort_rank=4,
        tests_passed=25000,
        tests_total=25000,
        p99_latency_ms=5.2,
        memory_leak_bytes=0,
        reviewer_verdict="3/3 Unanimous Blind Pass",
        hash=""
    )
    pr_2.hash = canonical_hash(get_proof_report_payload(pr_2))

    pr_3 = ProofReport(
        id="pr_3",
        worker_id=USR_WORKER_03,
        submission_id=None,
        sprint_name="Sprint #1: Zero-Copy Serialization & Socket Buffer I/O",
        completed_at=now - datetime.timedelta(days=30),
        score=95.8,
        cohort_rank=3,
        tests_passed=10000,
        tests_total=10000,
        p99_latency_ms=1.2,
        memory_leak_bytes=0,
        reviewer_verdict="3/3 Unanimous Blind Pass",
        hash=""
    )
    pr_3.hash = canonical_hash(get_proof_report_payload(pr_3))

    db.add_all([pr_1, pr_2, pr_3])
    db.flush()


def seed(db: Session):
    """Executes worker activity relations (Phase 40) and proof reports (Phase 50)."""
    seed_relations(db)
    seed_proof_reports(db)


def run(db: Session):
    seed(db)

