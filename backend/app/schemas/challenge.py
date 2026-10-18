from typing import Optional, List, Dict, Any
import datetime
from backend.app.schemas.base import CamelModel

class ChallengeResponse(CamelModel):
    id: str
    venture_id: str
    role_id: str
    title: str
    duration_hours: int
    starts_at: Optional[datetime.datetime] = None
    ends_at: Optional[datetime.datetime] = None
    status: str
    created_at: Optional[datetime.datetime] = None

class ScoreRequest(CamelModel):
    vector_scores: Dict[str, float]
    reviewer_verdict: Optional[str] = "Benchmarked and cryptographically attested."

class SubmissionResponse(CamelModel):
    id: str
    challenge_id: str
    worker_id: str
    candidate_code: str
    status: str
    score: float
    p99_latency_ms: float
    tests_passed: int
    tests_total: int
    hash: str
    replay_integrity: float
    failure_recovery: float
    concurrency_latency: float
    code_elegance: float
    reviewer_verdict: str
    signed_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None

class ProofReportResponse(CamelModel):
    id: str
    worker_id: str
    submission_id: Optional[str] = None
    sprint_name: str
    completed_at: Optional[datetime.datetime] = None
    score: float
    cohort_rank: str
    hash: str
    tests_passed: int
    tests_total: int
    p99_latency_ms: float
    memory_leak_bytes: int
    reviewer_verdict: str
    created_at: Optional[datetime.datetime] = None

class WorkerProofOfWorkResponse(CamelModel):
    items: List[ProofReportResponse]
    total: int
    merkle_root: Optional[str] = "0x4b7f892a01c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4"
