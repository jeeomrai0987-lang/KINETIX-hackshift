# VentureForge AI — Worker Database Architecture & Data Notes (Person B)

## 1. Scope & Ownership
This document specifies the Worker domain data layer owned by **Person B**, implementing the contracts agreed in `docs/SHARED_CONTRACT.md`.

Owned files:
- `database/models/worker_profile.py`: Worker profile data model.
- `database/models/worker_activity.py`: Worker activity, invitations, applications, submissions, proof reports.
- `database/seed/seed_worker_people.py`: Phase 10 seed for worker candidate users.
- `database/seed/seed_worker_profiles.py`: Phase 20 seed for 1:1 worker profiles.
- `database/seed/seed_worker_activity.py`: Phase 40/50 seed for invitations, applications, submissions, and proof reports.
- `database/queries/worker.py`: Query abstractions for worker profiles and portal dashboards.
- `database/tests/test_worker_profiles.py`: Automated unit tests for worker profiles.
- `database/tests/test_worker_activity.py`: Automated tests for FK resolution, unique constraints, and canonical hashes.
- `docs/DATA_NOTES_WORKER.md`: Technical documentation for the worker database domain.

---

## 2. Table Definition: `worker_profiles`

| Column | Type | Constraints / Defaults | Description |
|---|---|---|---|
| `user_id` | `String(64)` | PK, FK -> `users.id` (ON DELETE CASCADE) | 1:1 link to worker user |
| `created_at` | `DateTime` | UTC timestamp | Creation time |
| `updated_at` | `DateTime` | UTC timestamp, onupdate=utcnow | Last modification time |
| `experience_level` | `String(32)` | default="mid" | One of: `junior`, `mid`, `senior`, `founding` |
| `skills` | `JSON` | default=list | JSON list of string skills (e.g. `["Rust", "Distributed Systems"]`) |
| `portfolio_url` | `String(512)` | nullable | Verifiable personal site or portfolio link |
| `github_url` | `String(512)` | nullable | Developer code repository link |
| `phone` | `String(32)` | nullable | Contact number for WhatsApp automated screening dispatch |
| `whatsapp_enabled` | `Boolean` | default=True | Flag enabling async WhatsApp sprint prompts & reminders |
| `cloaked` | `Boolean` | **default=True** | Zero-bias anonymity shield (founders see only candidate codes until reveal) |
| `weekly_availability_hours` | `Integer` | default=20 | Available sprint bandwidth per week |
| `percentile` | `Float` | default=95.0 | Cognitive / benchmark percentile rank across cohort |

---

## 3. Table Definitions: Worker Activity (`worker_activity.py`)

### `submissions`
| Column | Type | Constraints / Index | Description |
|---|---|---|---|
| `id` | `String(64)` | PK | Stable ID (e.g. `sub_01`) |
| `created_at` | `DateTime` | UTC timestamp | Submission timestamp |
| `challenge_id` | `String(64)` | FK -> `challenges.id` (ON DELETE CASCADE), indexed | Challenge evaluated |
| `worker_id` | `String(64)` | FK -> `users.id` (ON DELETE CASCADE), indexed | Worker candidate |
| `candidate_code` | `String(64)` | — | Blind alias (e.g. `Candidate #TX-9042A`) |
| `status` | `String(32)` | indexed, default="in_review" | `in_review` or `attested` |
| `score` | `Float` | — | Overall weighted benchmark score (0.0 to 100.0) |
| `p99_latency_ms` | `Float` | — | Benchmark P99 latency metric |
| `tests_passed` | `Integer` | — | Successful test executions |
| `tests_total` | `Integer` | — | Total test suite executions |
| `hash` | `String(128)` | — | Cryptographic SHA-256 (`0x` + hex) of canonical payload |
| `replay_integrity` | `Float` | — | Vector score: Replay determinism (35% weight) |
| `failure_recovery` | `Float` | — | Vector score: Fault recovery (30% weight) |
| `concurrency_latency` | `Float` | — | Vector score: Concurrency latency (20% weight) |
| `code_elegance` | `Float` | — | Vector score: Code design & documentation (15% weight) |
| `reviewer_verdict` | `String(255)` | — | Evaluation verdict (e.g. `3/3 Unanimous Blind Pass`) |
| `signed_at` | `DateTime` | nullable | Attestation ledger signature timestamp |

### `proof_reports`
| Column | Type | Constraints / Index | Description |
|---|---|---|---|
| `id` | `String(64)` | PK | Stable ID (e.g. `pr_1`) |
| `created_at` | `DateTime` | UTC timestamp | Record creation time |
| `worker_id` | `String(64)` | FK -> `users.id` (ON DELETE CASCADE), indexed | Recipient worker |
| `submission_id` | `String(64)` | FK -> `submissions.id` (ON DELETE SET NULL), nullable, indexed | Optional linked challenge submission |
| `sprint_name` | `String(255)` | — | Sprint milestone name |
| `completed_at` | `DateTime` | — | Completion timestamp |
| `score` | `Float` | — | Attested score |
| `cohort_rank` | `String(64)` | — | Standing (e.g. `Rank #2 in Cohort`) |
| `hash` | `String(128)` | — | Cryptographic SHA-256 (`0x` + hex) of canonical report payload |
| `tests_passed` | `Integer` | — | Tests passed |
| `tests_total` | `Integer` | — | Total tests |
| `p99_latency_ms` | `Float` | — | Attested latency |
| `memory_leak_bytes` | `Integer` | default=0 | Zero memory leak proof |
| `reviewer_verdict` | `String(255)` | — | Committee verdict |

### `invitations`
| Column | Type | Constraints / Index | Description |
|---|---|---|---|
| `id` | `String(64)` | PK | Stable ID (e.g. `inv_1`) |
| `created_at` | `DateTime` | UTC timestamp | Dispatched timestamp |
| `venture_id` | `String(64)` | FK -> `ventures.id` (ON DELETE CASCADE), indexed | Sponsoring venture |
| `role_id` | `String(64)` | FK -> `squad_roles.id` (ON DELETE CASCADE), indexed | Targeted squad role |
| `worker_id` | `String(64)` | FK -> `users.id` (ON DELETE CASCADE), indexed | Invited candidate |
| `equity_pct` | `Float` | — | Offered equity percentage (e.g. `15.0`) |
| `terms` | `Text` | — | Vesting & SAFE protection terms |
| `message` | `Text` | — | Founder message |
| `status` | `String(32)` | indexed, default="pending" | `pending`, `accepted`, `declined` |
| `responded_at` | `DateTime` | nullable | Response timestamp |
*Constraint: `UniqueConstraint("role_id", "worker_id", name="uq_invitation_role_worker")`*

### `applications`
| Column | Type | Constraints / Index | Description |
|---|---|---|---|
| `id` | `String(64)` | PK | Stable ID (e.g. `app_1`) |
| `created_at` | `DateTime` | UTC timestamp | Submission timestamp |
| `role_id` | `String(64)` | FK -> `squad_roles.id` (ON DELETE CASCADE), indexed | Applied squad role |
| `worker_id` | `String(64)` | FK -> `users.id` (ON DELETE CASCADE), indexed | Applicant worker |
| `blind_token` | `String(64)` | — | Blind application token (e.g. `BLIND-TOK-8821B`) |
| `status` | `String(32)` | indexed, default="submitted" | `submitted` or `reviewed` |
*Constraint: `UniqueConstraint("role_id", "worker_id", name="uq_application_role_worker")`*

---

## 4. Cryptographic Hash Invariant (Rule #2)
- All hashes on `submissions.hash` and `proof_reports.hash` are calculated strictly as `canonical_hash(payload)`:
  - Canonical JSON stringification: `json.dumps(payload, sort_keys=True, separators=(",", ":"))`
  - SHA-256 digest with prefix `0x` (yielding a 66-character lowercase hex string).
- In automated test suite `test_worker_activity.py`, every seeded hash is recalculated over the entity's payload and verified to equal the seeded hash byte-for-byte.

---

## 5. Seed Phases
- **PHASE 10 (`seed_worker_people.py`)**:
  - Seeds worker candidate users into `users`: `usr_worker_03` (Elena Vance), `usr_worker_04` (Julian Vance), `usr_worker_05` (Elena Rostova), `usr_worker_extra_1`, `usr_worker_extra_2`, `usr_worker_extra_3`.
- **PHASE 20 (`seed_worker_profiles.py`)**:
  - Seeds 1:1 `WorkerProfile` records matching `WorkerProfile.jsx` and `WorkerSettings.jsx`.
- **PHASE 40 & 50 (`seed_worker_activity.py`)**:
  - Seeds pending invitations (`inv_1`, `inv_2`, `inv_3`), blind applications (`app_1`, `app_2`), sprint challenge submissions (`sub_01`, `sub_02`, `sub_03`), and verified proof-of-work telemetry reports (`pr_1`, `pr_2`, `pr_3`).
