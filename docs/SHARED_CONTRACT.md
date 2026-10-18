# VentureForge AI — Shared Contract (database <-> backend <-> frontend)

Both laptops read this file. **Do not change it without telling the other person**; if you must change it, edit it in its own small PR (`docs: contract change — <what>`) and message your partner before merging.

Source of truth for the entities: the mock data currently hard-coded in `src/pages/**` (every page has a `const [...] = [` array or a `useState([...])`). Where this contract and the mock data disagree, the contract wins and the frontend gets wired to the API later.

---

## 1. Who owns what (this is what prevents merge conflicts)

| Area | Person A — Database | Person B — Backend |
|---|---|---|
| `database/**` | OWNS | read-only (import it) |
| `backend/**` | read-only | OWNS |
| `docs/SHARED_CONTRACT.md` | change only via PR + heads-up | change only via PR + heads-up |
| `.env.example`, `.gitignore`, `package.json`, `vite.config.js`, root `README.md` run section | no | OWNS |
| `src/api/**` (new), `src/context/AuthContext.jsx`, `src/components/auth/**` (new), `src/App.jsx`, `src/components/common/Toast.jsx` | no | OWNS |
| `src/pages/auth/**`, `src/pages/founder/**`, `src/components/layout/FounderLayout.jsx` | no | OWNS (Phase 3) |
| `src/pages/worker/**`, `src/components/layout/WorkerLayout.jsx` | OWNS (Phase 3) | no |
| `src/pages/investor/**`, `src/components/layout/InvestorLayout.jsx` | OWNS (Phase 3) | no |
| `src/pages/public/**` | nobody for now | nobody for now |

Rule: if a file is not in your column, you do not edit it. Need a change there? Ask the owner.

## 2. Git workflow (two laptops, one repo)

- `main` is always runnable. Never force-push `main`.
- Person A works on `feat/database`, Person B on `feat/backend`. Phase 3 branches: `feat/wire-worker-investor` (A), `feat/wire-founder-auth` (B).
- Commit small and often. Prefix: `db:`, `api:`, `wire:`, `docs:`, `fix:`.
- Before starting work and before every push: `git fetch origin && git rebase origin/main` (or `git pull --rebase origin main`).
- Merge to `main` through a PR at least at the end of each phase (section 8). The other person pulls `main` right after.
- Never commit: `.env`, `*.db`, `venv/`, `node_modules/`, `dist/`. Commit `.env.example` only.
- Both people run the same seed script, so both laptops show identical demo data.

## 3. Stack decisions (fixed)

- Frontend: existing React 18 + Vite 6 + Tailwind + React Router (port **3000**).
- Backend: **Python 3.11+, FastAPI, Pydantic v2, uvicorn** (port **8000**). The existing `.gitignore` already expects a Python `backend/` with a `venv/` and `*.db` files.
- Database layer: **SQLAlchemy 2.0 (typed `Mapped[...]` style) + Alembic**, in the top-level `database/` package.
- DB engine: **SQLite by default** (`DATABASE_URL=sqlite:///./ventureforge.db`, file created at repo root, already git-ignored via `*.db`). Everything must also work on PostgreSQL by changing only `DATABASE_URL` — so no SQLite-only features, use portable column types, and store lists/objects in JSON columns.
- Auth: email + password, **bcrypt** hashes, **JWT** bearer tokens.
- Run from the **repo root** so both packages import cleanly:
  - `pip install -r database/requirements.txt -r backend/requirements.txt`
  - `python -m database.seed` (creates tables via Alembic + loads demo data)
  - `uvicorn backend.app.main:app --reload --port 8000`
  - `npm run dev` (Vite proxies `/api` to `http://localhost:8000`)
- Import contract: the backend imports **only** from `database` via `from database.session import get_db, SessionLocal` and `from database import models`. Nothing else crosses the boundary.

## 4. Environment variables (`.env.example`, owned by Person B)

```
ENV=development               # `/auth/demo/{role}` is disabled when ENV=production
DATABASE_URL=sqlite:///./ventureforge.db
JWT_SECRET=change-me-in-real-env
JWT_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=               # optional; AI endpoints fall back to deterministic logic when empty
GEMINI_MODEL=                  # e.g. gemini-2.5-flash
GEMINI_RERANK=false            # optional AI candidate re-ranking (defaults to deterministic scoring)
```

## 5. Data model (names are fixed; snake_case in DB, camelCase in JSON)

General rules: primary keys are **strings** (`id`), seed rows use the stable readable ids listed in section 7 and new rows get `<prefix>_<uuid4 hex[:12]>`. Money is **integer cents** (`*_cents`). Percentages are numbers (`equity_pct = 15.0` means 15%). Timestamps are UTC, ISO-8601 in JSON. Every table has `created_at`; add `updated_at` where rows are edited.

| Table | Columns (besides `id`, `created_at`) |
|---|---|
| `cohorts` | `name`, `batch_no` |
| `users` | `email` (unique), `password_hash`, `name`, `role` (`founder`/`investor`/`worker`), `title`, `avatar_url`, `node_id`, `verified` (bool), `cohort_id` -> cohorts |
| `worker_profiles` | `user_id` (PK, -> users), `experience_level` (`junior`/`mid`/`senior`/`founding`), `skills` (JSON list of str), `portfolio_url`, `github_url`, `phone`, `whatsapp_enabled`, `cloaked` (default true), `weekly_availability_hours`, `percentile` |
| `investor_profiles` | `user_id` (PK, -> users), `tier`, `wallet_address`, `preferred_sectors` (JSON list), `instant_alerts`, `weekly_digest`, `accreditation_status` (`pending`/`verified`/`expired`), `accreditation_expires_at` |
| `ventures` | `founder_id` -> users, `cohort_id`, `name`, `thesis` (text), `sector`, `stage`, `clarity_score`, `constraints` (JSON: latency, compliance, squadSize…), `raised_cents`, `runway_months`, `mrr_cents`, `status` |
| `squad_roles` | `venture_id`, `title`, `description`, `equity_pct`, `status` (`filled`/`vacant`/`reserved`), `filled_by_user_id` (nullable), `requirements` (JSON list) |
| `matches` | `venture_id`, `role_id`, `worker_id`, `candidate_code`, `synergy_score`, `fit_details`, `status` (`suggested`/`invited`/`declined`) |
| `challenges` | `venture_id`, `role_id`, `title`, `duration_hours` (default 48), `starts_at`, `ends_at`, `status` (`open`/`closed`) |
| `submissions` | `challenge_id`, `worker_id`, `candidate_code`, `status` (`in_review`/`attested`), `score`, `p99_latency_ms`, `tests_passed`, `tests_total`, `hash`, `replay_integrity`, `failure_recovery`, `concurrency_latency`, `code_elegance`, `reviewer_verdict`, `signed_at` (nullable) |
| `proof_reports` | `worker_id`, `submission_id` (nullable), `sprint_name`, `completed_at`, `score`, `cohort_rank`, `hash`, `tests_passed`, `tests_total`, `p99_latency_ms`, `memory_leak_bytes`, `reviewer_verdict` |
| `invitations` | `venture_id`, `role_id`, `worker_id`, `equity_pct`, `terms`, `message`, `status` (`pending`/`accepted`/`declined`), `responded_at` |
| `applications` | `role_id`, `worker_id`, `blind_token`, `status` (`submitted`/`reviewed`) |
| `cap_table_entries` | `venture_id`, `holder_user_id` (nullable), `holder_label`, `equity_pct`, `kind` (`founder`/`cofounder`/`reserve`/`option_pool`/`investor_safe`), `vested_pct` |
| `restructuring_events` | `venture_id`, `type`, `from_user_id`, `to_user_id`, `equity_delta_pct`, `stage`, `note`, `executed_at` (nullable) |
| `transactions` | `venture_id`, `occurred_on`, `description`, `category` (`infrastructure`/`revenue`/`payroll`/`legal`/`other`), `amount_cents` (signed), `proof_hash` |
| `financial_snapshots` | `venture_id`, `month` (`YYYY-MM`), `burn_cents`, `revenue_cents`, `cash_cents` |
| `funding_opportunities` | `name`, `category` (`syndicate`/`micro_vc`/`grant`), `check_min_cents`, `check_max_cents`, `structure`, `tags` (JSON), `timeline`, `base_fit_pct` |
| `funding_requests` | `venture_id`, `funding_opportunity_id`, `status` |
| `investments` | `investor_id`, `venture_id`, `instrument_type` (`safe`/`grant`), `instrument_label`, `principal_cents`, `val_cap_cents`, `discount_pct`, `equity_pct`, `contract_addr`, `signed_on`, `status` |
| `milestone_updates` | `venture_id`, `headline`, `body`, `stage_label`, `tag`, `merkle_proof`, `deliverables`, `metrics` (JSON), `published_at` |
| `milestone_reads` | `investor_id`, `update_id` (composite PK) |
| `disclosure_requests` | `investor_id`, `venture_id`, `status` |
| `notifications` | `user_id`, `kind`, `body`, `read` |
| `audit_log` | `actor_id`, `action`, `entity`, `entity_id`, `payload` (JSON) |

Required indexes/constraints: unique `users.email`; unique `(role_id, worker_id)` on `matches`, `invitations`, `applications`; index on every `venture_id`, `worker_id`, `investor_id`, `status` column used in a filter; FK `ON DELETE CASCADE` from ventures to its children.

## 6. Business rules both sides must respect

1. **Blind protocol.** A founder never receives a candidate's real `name`, `email`, `avatar_url` or `phone` until that candidate's invitation is `accepted`. Before that, founder-facing payloads contain `candidateCode` only (e.g. `TX-9042A`). The backend enforces this in the serializer, not just in the UI. The current frontend leaks names next to codes (see REVIEW.md) — the data layer must never make that possible.
2. **Real hashes.** `submissions.hash` / `proof_reports.hash` = SHA-256 (hex, `0x` prefix) of the canonical JSON of the scored payload, computed server-side. Blockchain/Arbitrum/Merkle-on-chain items stay simulated and must be labelled as simulated in the UI.
3. **Cap table integrity.** For one venture, `sum(equity_pct)` over `cap_table_entries` must equal 100.0 (tolerance 0.001). Accepting an invitation and executing a restructuring each run in a **single DB transaction** that moves equity and keeps the sum at 100.
4. **Role isolation.** Founders only see their own ventures; workers only their own invitations/applications/reports; investors only their own investments (and published milestone updates of ventures they hold).
5. **Audit.** Every state change on invitations, submissions (score/sign), cap table, restructuring and funding requests writes an `audit_log` row.

## 7. Demo cast (seed must create exactly this; used by both laptops)

One consistent cast replaces the contradicting names in the current mock data.

| id | Name | Role | Notes |
|---|---|---|---|
| `usr_founder_01` | Alex Mercer | founder | `alex.mercer@synthetix.ai`, CEO of venture `ven_synthetix` (Synthetix AI), node `NODE-FND-0001` |
| `usr_worker_03` | Elena Vance | worker | `elena.vance@startup.io`, candidate code `TX-5512B`, skills Distributed Systems/Rust/Go/System Architecture |
| `usr_investor_02` | Marcus Vance | investor | `marcus.vance@angelsyndicate.vc`, tier "Syndicate Tier 1" |
| `usr_worker_04` | Julian Vance | worker | candidate code `TX-9042A` |
| `usr_worker_05` | Elena Rostova | worker | candidate code `TX-8821B` |
| `usr_cofounder_01` | Marcus Chen | founder (CTO of Synthetix) | filled role |
| `usr_cofounder_02` | Sarah Jenkins | founder (Head of Enterprise Growth) | filled role |

All demo accounts share the password `Demo#2026` (hashed in the seed; never shown in the UI). Other ventures to seed: `ven_polymatrix` (PolyMatrix AI), `ven_chronodb` (ChronoDB), `ven_aether` (Aether Labs), `ven_kauri` (Kauri Health) with their CEOs as extra founder users. Seed the rest of the data (roles, matches, submissions, invitations, transactions, 6 months of snapshots, funding opportunities, investments, milestone updates) from the arrays in `src/pages/**` — same numbers, converted to the units in section 5.

## 8. REST API (`/api/v1`, JSON, camelCase)

Conventions: `Authorization: Bearer <jwt>`; errors are `{"error": {"code": "string", "message": "string"}}` with a proper HTTP status; list endpoints return `{"items": [...], "total": n}`; all endpoints are role-guarded; OpenAPI docs at `/docs`; health check `GET /health`.

**Auth**
- `POST /auth/register` `{name,email,password,role,skills?,portfolioUrl?,experienceLevel?,whatsappEnabled?}` -> `{token,user}`
- `POST /auth/login` `{email,password}` -> `{token,user}`
- `POST /auth/demo/{role}` -> `{token,user}` (only when `ENV != production`)
- `GET /auth/me` -> `user`

**Founder** (`role=founder`)
- `GET /ventures/mine`, `POST /ventures`, `PUT /ventures/{id}`
- `GET /ventures/{id}/dashboard` (squad synergy, runway, sprint clock, roster, cohort feed)
- `POST /ventures/{id}/decompose` `{thesis}` -> constraints + squad blueprint (LLM if key set, deterministic fallback otherwise)
- `POST /ventures/{id}/blueprint/approve` -> creates/updates `squad_roles`, triggers a match run
- `GET /ventures/{id}/matches`, `POST /ventures/{id}/matches/rerun`, `POST /matches/{id}/invite`
- `GET /ventures/{id}/challenge`, `GET /challenges/{id}/submissions`, `POST /submissions/{id}/score` `{vectorScores}`, `POST /submissions/{id}/sign`
- `GET /submissions/{id}/proof`
- `GET /ventures/{id}/restructuring`, `POST /ventures/{id}/restructuring/execute`
- `GET /ventures/{id}/funding-opportunities?category=`, `POST /funding-opportunities/{id}/request`
- `GET /ventures/{id}/financials?range=6m`, `GET /ventures/{id}/transactions`, `GET /ventures/{id}/cap-table`, `GET /ventures/{id}/financials/export.csv`

**Worker** (`role=worker`)
- `GET /worker/dashboard`, `GET|PUT /worker/profile`, `GET|PUT /worker/settings`
- `GET /worker/opportunities`, `POST /worker/opportunities/refresh`, `POST /worker/opportunities/{roleId}/apply`
- `GET /worker/invitations?status=`, `POST /invitations/{id}/accept`, `POST /invitations/{id}/decline`
- `GET /worker/proof-of-work`

**Investor** (`role=investor`)
- `GET /investor/dashboard`, `GET /investor/portfolio`, `GET /investor/updates`, `POST /investor/updates/{id}/read`
- `GET /investor/financial-reports`, `GET /investor/instruments`, `GET /investor/discover`
- `POST /investor/disclosure-requests`, `GET|PUT /investor/settings`, `POST /investor/settings/recertify`

Every endpoint above must return JSON shaped so a page can drop its current mock array and render without reshaping (numbers raw; the **frontend** formats `$`, `%`, dates).

## 9. Phases (merge to `main` at the end of each)

- **P0 (together, 10 min):** one person commits this `docs/` folder to `main`; the other pulls. Agree on who is A and who is B.
- **P1 (parallel):** A pushes `database/models.py` + `database/session.py` **first (within ~45 minutes)** so B can import them; then Alembic migration + seed. B scaffolds FastAPI, config, auth (register/login/me), schemas and the router skeletons.
- **P2 (parallel):** A: seed completeness, constraints, `database/queries/*` helpers if B asks, DB tests. B: all routers, rules from section 6, AI service, tests.
- **P3 (parallel, disjoint files):** wire the frontend. A wires worker + investor pages and their layouts; B wires auth, founder pages, App.jsx, ProtectedRoute. Replace each page's mock array with `src/api/*` calls plus loading / error / empty states.
- **P4 (together):** one clean clone on each laptop, run the section 3 commands from scratch, click through all three portals, fix leftovers, tag `v0.1-demo`.
