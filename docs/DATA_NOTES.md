# VentureForge AI — Founder Database Architecture & Data Notes

Documented by: **Person A (Founder Database Engineer)**  
Target branch: `feat/db-founder`  
Scope: top-level `database/` package, founder models, seeds, queries, and Alembic migrations.

---

## 1. Table Schemas & Relationships

The database layer implements typed SQLAlchemy 2.0 (`Mapped[...]`) models configured for portability across SQLite and PostgreSQL.

```
 cohorts (1) ────< (N) users (1) ────< (N) ventures (1) ────< (N) squad_roles (1) ────< (N) challenges
                         │                     │                        │
                         │                     ├────< (N) cap_table     ├────< (N) matches
                         │                     ├────< (N) snapshots     └────< (N) applications
                         │                     ├────< (N) transactions
                         │                     ├────< (N) restructurings
                         │                     └────< (N) milestone_updates
                         │
                         ├──── (1:1) investor_profiles
                         ├──── (1:1) worker_profiles
                         ├────< (N) investments
                         ├────< (N) notifications
                         └────< (N) audit_log
```

### Core Tables (`database/models/core.py`)
- `cohorts`: Accelerator batches (e.g. `coh_alpha25` - Cohort Alpha '25, batch 204).
- `users`: Universal identity table. Unique `email`, bcrypt `password_hash`, role (`founder`, `investor`, `worker`), `node_id`, and `verified` boolean.
- `notifications`: User-facing alert stream with `kind`, `body`, and boolean `read` flag.
- `audit_log`: Immutable change log tracking actor ID, action, entity, entity ID, and JSON payload.

### Venture Tables (`database/models/venture.py`)
- `ventures`: Core startup entity (`ven_synthetix`, `ven_polymatrix`, etc.) linked to founder (`users.id`). Stores clarity score, JSON constraints, and metrics.
- `squad_roles`: Role definitions for team construction (`filled`, `vacant`, `reserved`), target `equity_pct`, requirements JSON, and optional `filled_by_user_id`.
- `challenges`: Technical sprint assessments (48-hour challenges) linked to ventures and squad roles.
- `matches`: Algorithmic pairing between squad roles and workers. Tracks candidate code (`TX-5512B`), `synergy_score`, and fit vectors.

### Finance Tables (`database/models/finance.py`)
- `cap_table_entries`: Equity distribution per venture. Sum of `equity_pct` must equal 100.0%.
- `restructuring_events`: Historical record of equity reallocations, dilution, or transfers.
- `transactions`: Immutable financial ledger for operational burn, income, and payroll. Stores SHA-256 `proof_hash`.
- `financial_snapshots`: Monthly accounting snapshots (`burn_cents`, `revenue_cents`, `cash_cents`) over a 6-month trailing period.
- `funding_opportunities`: Grants, syndicate pools, and micro-VC opportunities.
- `funding_requests`: Applications from ventures to specific funding opportunities.

### Investor Tables (`database/models/investor.py`)
- `investor_profiles`: Investor metadata, tier, accreditation status, alert settings, and wallet addresses.
- `investments`: Legal and economic contracts (SAFEs, grants) linking investor users to ventures.
- `milestone_updates`: Cryptographically proven venture sprint milestones with Merkle roots, metrics, and deliverables.
- `milestone_reads`: Read receipts tracking investor engagement.
- `disclosure_requests`: Access requests for restricted venture financials.

---

## 2. Units & Conventions

To prevent rounding and floating-point errors across database, API, and frontend layers:

| Field Pattern | Data Type in DB | Unit / Format | Example |
|---|---|---|---|
| `*_cents` | `Integer` | Currency cents (1/100 USD) | `$500,000.00` is stored as `50000000` |
| `*_pct` | `Float` | Percentage number (0.0 to 100.0) | `42.5%` is stored as `42.5` |
| Timestamps | `DateTime(timezone=True)` | UTC ISO-8601 | `2026-10-18T04:26:08Z` |
| IDs | `String(36)` | String prefix + readable ID or UUID hex | `usr_founder_01`, `ven_synthetix`, `rst_a1b2c3d4e5f6` |
| JSON columns | `sa.JSON` | Portable JSON array or object | `["Rust", "Distributed Systems"]` |
| Hashes | `String(66)` | Hexadecimal SHA-256 with `0x` prefix | `0x5d41402abc4b2a76b9719d911017c592...` |

---

## 3. Seed Dataset & Demo Cast

Seed execution is orchestrated via phased modules:
```
python -m database.seed --reset
```

### Demo Accounts (`password: Demo#2026` for all)
- `usr_founder_01` (`alex.mercer@synthetix.ai`): Alex Mercer, CEO of Synthetix AI (`NODE-FND-0001`).
- `usr_cofounder_01` (`marcus.chen@synthetix.ai`): Marcus Chen, CTO of Synthetix AI (`NODE-FND-0002`).
- `usr_cofounder_02` (`sarah.jenkins@synthetix.ai`): Sarah Jenkins, Head of Enterprise Growth (`NODE-FND-0003`).
- `usr_investor_02` (`marcus.vance@angelsyndicate.vc`): Marcus Vance, Syndicate Tier 1 Investor (`NODE-INV-8841Z`).
- Additional venture CEOs: Dr. Aaron Meyer (PolyMatrix), Vikram Joshi (ChronoDB), Dr. Maya Lin (Kauri Health), Liam Thorne (Aether Labs).

### Ventures
1. **Synthetix AI** (`ven_synthetix`): Enterprise Cognitive Mesh & Neural Agent Orchestration.
   - Raised: $500,000 (`50000000` cents), MRR: $8,500 (`850000` cents), Runway: 16 months.
2. **PolyMatrix AI** (`ven_polymatrix`): Autonomous Material Synthesis.
3. **ChronoDB** (`ven_chronodb`): High-frequency time-series vector store.
4. **Aether Labs** (`ven_aether`): Decentralized compute scheduling.
5. **Kauri Health** (`ven_kauri`): Privacy-preserving genomic diagnostics.

### Cap Table Breakdown for Synthetix AI
- Alex Mercer (CEO, Founder): **42.5%** (25.0% vested)
- Marcus Chen (CTO, Co-Founder): **32.0%** (20.0% vested)
- Sarah Jenkins (Growth, Co-Founder): **10.5%** (15.0% vested)
- Open Founding Reserve / Option Pool: **15.0%** (0.0% vested)
- **Total: 100.0%** (strictly enforced)

---

## 4. Contract Rule Enforcement

### Blind Protocol (Section 6 Rule 1)
- The database model for `matches` stores `candidate_code` (e.g. `TX-5512B`).
- `database/queries/founder.py::get_blind_matches_for_venture` explicitly selects only the candidate code, synergy score, status, and fit details. Sensitive PII (`name`, `email`, `phone`, `avatar_url`) is never queried or returned to founder callers before invitation acceptance.

### Cap Table Integrity (Section 6 Rule 3)
- Helper function `founder.validate_cap_table_integrity(db, venture_id)` validates `abs(sum(equity_pct) - 100.0) < 0.001`.
- `founder.execute_equity_transfer(...)` executes within a single database transaction, reallocates equity atomically, checks the 100.0% invariant, and commits an `audit_log` and `restructuring_events` row.

---

## 5. Alembic Migrations

- Configured at repo root via `alembic.ini`.
- Version scripts stored in `database/alembic/versions/`.
- Target metadata dynamically loads all models from `database.models`.
- SQLite batch mode enabled for seamless schema adjustments.
- Run migrations:
  ```bash
  alembic upgrade head
  ```
