# VentureForge AI — Founder Database Architecture & Data Notes

Documented by: **Person A (Founder Database Engineer)**  
Target branch: `feat/db-founder`  
Scope: Top-level `database/` package, founder models, seeds, queries, Alembic migrations, and backend contract integration.

---

## 1. Table Schemas & Relationships (ER Summary)

The database layer implements typed SQLAlchemy 2.0 (`Mapped[...]`) models configured for complete portability across SQLite and PostgreSQL.

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
- `cohorts`: Accelerator batches (e.g. `coh_alpha25` — Cohort Alpha '25, batch 204).
- `users`: Universal identity table. Unique `email`, bcrypt `password_hash`, role (`founder`, `investor`, `worker`), `node_id`, and `verified` boolean.
- `notifications`: User-facing alert stream with `kind`, `body`, and boolean `read` flag.
- `audit_log`: Immutable change log tracking actor ID, action, entity, entity ID, and JSON payload.

### Venture Tables (`database/models/venture.py`)
- `ventures`: Core startup entity (`ven_synthetix`, `ven_polymatrix`, etc.) linked to founder (`users.id`). Stores clarity score, JSON constraints, and metrics.
- `squad_roles`: Role definitions for team construction (`filled`, `vacant`, `reserved`), target `equity_pct`, requirements JSON, and optional `filled_by_user_id`.
- `challenges`: Technical sprint assessments (48-hour challenges) linked to ventures and squad roles.
- `matches`: Algorithmic pairing between squad roles and workers. Unique `(role_id, worker_id)`, tracks candidate code (`TX-5512B`), `synergy_score`, and fit vectors.

### Finance Tables (`database/models/finance.py`)
- `cap_table_entries`: Equity distribution per venture. Sum of `equity_pct` must equal exactly 100.0%.
- `restructuring_events`: Historical record of equity reallocations, dilution, or transfers.
- `transactions`: Immutable financial ledger for operational burn, income, and payroll. Stores SHA-256 `proof_hash` (66 characters, `0x`-prefixed).
- `financial_snapshots`: Monthly accounting snapshots (`burn_cents`, `revenue_cents`, `cash_cents`) over a 6-month trailing period.
- `funding_opportunities`: Grants, syndicate pools, and micro-VC opportunities.
- `funding_requests`: Applications from ventures to specific funding opportunities.

### Investor Tables (`database/models/investor.py`)
- `investor_profiles`: Investor metadata, tier, accreditation status, alert settings, and wallet addresses.
- `investments`: Legal and economic contracts (SAFEs, grants) linking investor users to ventures.
- `milestone_updates`: Cryptographically proven venture sprint milestones with Merkle roots (`merkle_proof`), metrics, and deliverables.
- `milestone_reads`: Read receipts tracking investor engagement. Composite PK `(investor_id, update_id)`.
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
```bash
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

### The 4 Funding Opportunities (from `FounderFunding.jsx`)
1. `opp_1`: Syndicate Alpha Angel Pool (syndicate, $250k–$500k, 98% fit)
2. `opp_2`: Apex Horizon Capital (micro_vc, $400k, 95% fit)
3. `opp_3`: NSF SBIR Phase I AI Grant (grant, $275k non-dilutive, 92% fit)
4. `opp_4`: Fintech Velocity Syndicate (syndicate, $150k–$300k, 91% fit)

---

## 4. SQLite / PostgreSQL Portability & Engine Quirks

To switch engines, change only `DATABASE_URL` (e.g. `postgresql://user:pass@localhost:5432/ventureforge`):

1. **Foreign Key Enforcement**:
   - SQLite disables foreign keys by default. `database/session.py` binds a connection listener that executes `PRAGMA foreign_keys=ON` automatically on every SQLite connection.
   - During seed reset (`--reset`), SQLite foreign keys are toggled off temporarily during table teardown to prevent dependency cascade locks, then toggled back on.
2. **Enum Portability**:
   - Instead of dialect-dependent native enum types (which create un-droppable PostgreSQL custom types and cause SQLite syntax failures), all constrained fields use explicit SQL `CheckConstraint`:
     - `role IN ('founder', 'investor', 'worker')`
     - `status IN ('filled', 'vacant', 'reserved')`
     - `category IN ('infrastructure', 'revenue', 'payroll', 'legal', 'other')`
3. **JSON Storage**:
   - Columns use generic `sqlalchemy.JSON`. In SQLite, arrays and dicts serialize as JSON strings. In PostgreSQL, they serialize as native `JSONB`.
4. **Timezones**:
   - All datetime columns use `DateTime(timezone=True)` with timezone-aware `datetime.now(timezone.utc)` defaults.

---

## 5. Query Helpers for Backend Engineers (`database.queries.founder`)

Backend routers should import helpers from `database.queries.founder` to avoid duplicating SQL and business logic:

```python
from database.session import get_db
from database.queries import founder

# 1. Cap table with total equity calculation:
entries, total_pct = founder.get_cap_table(db, venture_id="ven_synthetix")

# 2. Blind candidate matches (strips all worker PII):
matches = founder.get_candidate_matches(db, venture_id="ven_synthetix")

# 3. Comprehensive venture financials (runway, snapshots, txns, cap table):
financials = founder.get_venture_financials(db, venture_id="ven_synthetix")

# 4. Aggregated founder dashboard metrics:
summary = founder.get_founder_dashboard_summary(db, venture_id="ven_synthetix")

# 5. Atomic equity reallocation (verifies 100.0% invariant & logs audit):
event = founder.execute_equity_transfer(
    db=db,
    venture_id="ven_synthetix",
    from_entry_id="cap_synth_04",
    to_entry_id="cap_synth_01",
    equity_pct=2.0,
    actor_id="usr_founder_01",
    note="Transferred from option pool",
)
```

---

## 6. How to Reset & Verify the Database

```bash
# 1. Create schema and load demo seed data through Alembic:
python -m database.seed --reset

# 2. Run full pytest suite (14 tests covering FKs, cascades, cap table sum, hashes):
python -m pytest database/tests/ -v

# 3. Check Alembic migration status:
alembic current
```
