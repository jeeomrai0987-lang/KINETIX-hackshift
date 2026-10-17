# VentureForge AI — React Application

**VentureForge AI: Where Ideas Become Ventures** is an autonomous venture formation and co-founder intelligence platform.

This repository contains the complete conversion of the prototype static files into a high-performance **React + Vite + Tailwind CSS + React Router** application, featuring a dedicated **Authentication & Onboarding Engine**.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Build for Production
```bash
npm run build
```

---

## 🔐 Authentication & Onboarding Page (`/auth`, `/login`, `/register`)

The new authentication system includes:
- **Sign In & Sign Up Modes**: Toggle between Login and Registration with fluid transitions.
- **Role Selection Engine**:
  - 🚀 **Founder**: Build ventures, recruit co-founders, allocate cap table, and seek seed funding.
  - 💼 **Talent / Worker**: Build cloaked verified profile, participate in 48h blind challenges, receive founder invitations.
  - 📈 **Investor**: Monitor verified sprint telemetry, syndicate SAFEs, inspect audited financials.
- **One-Click Demo Evaluator Access**:
  - One-click instant login as **Founder (Elena Vance / Alex Mercer)**
  - One-click instant login as **Investor (Marcus Vance)**
  - One-click instant login as **Talent / Worker (Elena Vance / Alex Mercer)**
- **Interactive Security & Profile Controls**:
  - Show/Hide Password toggle with real-time enterprise password strength meter.
  - Interactive chip-tag manager for verified core skills (add with Enter, remove with 1 click).
  - Experience bracket selector (Junior, Mid, Senior, Founding).
  - WhatsApp Challenge Screening Dispatch toggle.
  - Form validation, error messaging, loading state indicators, and feedback toasts.
  - Role-based redirect to respective portal dashboard upon authentication.

---

## 🧭 Application Structure & Portals

### 1. Public & Auth
- **Landing Page** (`/`): Complete hero section, candidate synergy console, 5-step formation flywheel, feature cards, WhatsApp flow, live cohort ticker.
- **Authentication** (`/auth`): Full login, register, and demo selector.

### 2. Founder Portal (`/founder/*`)
- **Dashboard** (`/founder/dashboard`): Squad synergy telemetry, active sprint clock, burn runway, team roster, financial trajectory chart, cohort audit feed.
- **Startup Brief** (`/founder/startup`): Thesis synthesis, natural language requirement decomposition, target squad architecture generator.
- **Team Arena** (`/founder/arena`): AI candidate synthesis, synergy index scores, radar balance, blind matching.
- **Challenge** (`/founder/challenge`): 48h live sprint challenge evaluation, multi-vector scoring rubrics, zero-bias cryptographic judge signing.
- **Proof-of-Work** (`/founder/proofwork`): SHA-256 Merkle root verification, soak-test metrics, terminal logs, downloadable attestation pack.
- **Restructuring** (`/founder/restructuring`): Dynamic team restructuring, 5-stage succession pipeline, cap table rebalancing.
- **Funding Discovery** (`/founder/funding`): AI matched angel syndicates, micro-VCs, and non-dilutive government grants.
- **Financials** (`/founder/financial`): Runway modeling, burn rate telemetry, fully diluted cap table bar, transaction ledger.

### 3. Investor Portal (`/investor/*`)
- **Dashboard** (`/investor/dashboard`): Portfolio holdings, capital deployment metrics, unread milestone feed, disclosure requests.
- **Portfolio** (`/investor/portfolio`): Holding stakes, valuation caps, discount rates, equity positions, sector filters.
- **Startup Updates** (`/investor/startup`): Cryptographically verified milestone releases, Merkle proofs (Arbitrum L2), throughput benchmark curves.
- **Financial Reports** (`/investor/financial-report`): Monthly burn progression vs revenue, quarterly attestation packs, tax filings.
- **Investment Terms** (`/investor/investment-terms`): Standardized post-money SAFEs, MFN side letters, token warrants.
- **Discover Startups** (`/investor/discover-startups`): Vetted cohort squads (YC bound, blind evaluated, fast-track).
- **Settings** (`/investor/settings`): SEC 506(c) accreditation re-certify, preferred sectors, Web3 multi-sig vault address.

### 4. Worker / Talent Portal (`/worker/*`)
- **Dashboard** (`/worker/dashboard`): Talent node status, rubric percentile ranking (Top 4%), active sprint challenges, direct founder offers.
- **My Profile** (`/worker/profile`): Verified core competencies, zero-bias identity cloaking shield, portable credential export.
- **Opportunities** (`/worker/opportunities`): Matched squad openings, equity allocations, blind token applications.
- **Invitations** (`/worker/invitations`): Direct founder offers with equity terms, one-click offer acceptance into cap table.
- **Proof-of-Work Reports** (`/worker/proof-of-work`): Sprint attestation scorecards, Merkle root hash verification, test logs.
- **Settings** (`/worker/settings`): Cloaking shield toggles, WhatsApp dispatch phone integration, linked GitHub sandbox repo.

---

## 🛠️ Tech Stack
- **React 18**
- **Vite 6**
- **Tailwind CSS 3** (configured with exact design tokens, typography, and spacing from original prototype)
- **React Router DOM 6** (with backward-compatible redirects for legacy `.html` links)
- **Google Fonts Inter & Material Symbols Outlined**
- **AuthContext** with localStorage session persistence and role switching.
