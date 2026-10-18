import os
import sys
import json
import hashlib
import bcrypt
from datetime import datetime, timezone, timedelta

# Ensure repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.session import Base, engine, SessionLocal
from database import models

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def compute_hash(data: dict) -> str:
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def seed_database():
    print("Initializing tables via SQLAlchemy Base.metadata.create_all...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(models.User).filter_by(id="usr_founder_01").first():
            print("Database is already seeded with demo cast. Skipping re-seed.")
            return

        print("Seeding fresh demo cast and venture ecosystem...")
        now = datetime.now(timezone.utc)
        shared_password_hash = hash_password("Demo#2026")

        # 1. Cohorts
        cohort_alpha = models.Cohort(
            id="coh_alpha25",
            name="Cohort Alpha '25",
            batch_no=204,
            created_at=now - timedelta(days=90),
        )
        db.add(cohort_alpha)
        db.flush()

        # 2. Users (Section 7 Demo Cast)
        user_founder = models.User(
            id="usr_founder_01",
            email="alex.mercer@synthetix.ai",
            password_hash=shared_password_hash,
            name="Alex Mercer",
            role="founder",
            title="Founder & CEO",
            avatar_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCrFd9FXpH1DVp90x6QYI3kcBlABNYtgFYxaa-elUwjSWxyV56HX1Uir3Bo-JqKk3TkfehwV64tbjsMvhw9FVCYgdY2H_bGj_WUycEQb8Dik8Hw6UG-DAyLKzDMeTucfRCt_DgSFD6L_pCOl0A8YFS_ujCydDFtmuuoeY7hOIu_gb7QgAuFUQWPIUNLCYl78krYPxXqb-rVILLe9UGsKUdf2HDshK8T-ZrUTNmAMRphT1t5VEKD26jNtQ",
            node_id="NODE-FND-0001",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=60),
        )

        user_cto = models.User(
            id="usr_cofounder_01",
            email="marcus.chen@synthetix.ai",
            password_hash=shared_password_hash,
            name="Marcus Chen",
            role="founder",
            title="Co-Founder & CTO",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0002",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=55),
        )

        user_growth = models.User(
            id="usr_cofounder_02",
            email="sarah.jenkins@synthetix.ai",
            password_hash=shared_password_hash,
            name="Sarah Jenkins",
            role="founder",
            title="Head of Enterprise Growth",
            avatar_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0003",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=50),
        )

        user_worker_elena = models.User(
            id="usr_worker_03",
            email="elena.vance@startup.io",
            password_hash=shared_password_hash,
            name="Elena Vance",
            role="worker",
            title="Lead Distributed Systems Architect",
            avatar_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAXDAn8ZFbqaXgUtAZFPSAMimDjdAoYUtHj9L77g4tSh_dzBGXy6q7ARHBvvPaEiQBevjgoVWtUl1CPRgJcoZ_Gyr1x8Zo7gNTBlUQObPUZdavCilarTN6yVjeMbRs58962jPDHojUKOmZ_bPn3g6RPFzhAkTcS32gCbsLDrLoGoPt23xW2bo98EiFz6_G89_dt-TciA5PCjPGcobNbxFBrua1O80BXj8xC1JSaqoZGvJJLCVcC2Qyt0g",
            node_id="TX-5512B",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=45),
        )

        user_worker_julian = models.User(
            id="usr_worker_04",
            email="julian.vance@talenthub.io",
            password_hash=shared_password_hash,
            name="Julian Vance",
            role="worker",
            title="Senior High-Throughput Systems Engineer",
            avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=256&q=80",
            node_id="TX-9042A",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=40),
        )

        user_worker_rostova = models.User(
            id="usr_worker_05",
            email="elena.rostova@devmesh.net",
            password_hash=shared_password_hash,
            name="Elena Rostova",
            role="worker",
            title="Founding Cryptography & Sandbox Architect",
            avatar_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=256&q=80",
            node_id="TX-8821B",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=35),
        )

        user_investor = models.User(
            id="usr_investor_02",
            email="marcus.vance@angelsyndicate.vc",
            password_hash=shared_password_hash,
            name="Marcus Vance",
            role="investor",
            title="Investor / Angel Syndicate Partner",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-INV-8841Z",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=60),
        )

        # Extra Founders for secondary ventures
        user_founder_poly = models.User(
            id="usr_founder_02",
            email="aaron.meyer@polymatrix.ai",
            password_hash=shared_password_hash,
            name="Dr. Aaron Meyer",
            role="founder",
            title="Founder & CEO",
            avatar_url="https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0004",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=50),
        )

        user_founder_chrono = models.User(
            id="usr_founder_03",
            email="vikram.joshi@chronodb.io",
            password_hash=shared_password_hash,
            name="Vikram Joshi",
            role="founder",
            title="Founder & CEO",
            avatar_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0005",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=45),
        )

        user_founder_kauri = models.User(
            id="usr_founder_04",
            email="maya.lin@kaurihealth.org",
            password_hash=shared_password_hash,
            name="Dr. Maya Lin",
            role="founder",
            title="Founder & CEO",
            avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0006",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=40),
        )

        user_founder_aether = models.User(
            id="usr_founder_05",
            email="liam.thorne@aetherlabs.xyz",
            password_hash=shared_password_hash,
            name="Liam Thorne",
            role="founder",
            title="Founder & CEO",
            avatar_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=256&q=80",
            node_id="NODE-FND-0007",
            verified=True,
            cohort_id=cohort_alpha.id,
            created_at=now - timedelta(days=35),
        )

        db.add_all([
            user_founder, user_cto, user_growth,
            user_worker_elena, user_worker_julian, user_worker_rostova,
            user_investor, user_founder_poly, user_founder_chrono, user_founder_kauri, user_founder_aether
        ])
        db.flush()

        # 3. Worker Profiles
        db.add(models.WorkerProfile(
            user_id=user_worker_elena.id,
            experience_level="senior",
            skills=["Distributed Systems", "Rust", "Go", "System Architecture", "Low-Latency Networking"],
            portfolio_url="https://github.com/elenavance/microvm-mesh",
            github_url="https://github.com/elenavance",
            phone="+1-415-555-0199",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=40,
            percentile=96.4,
            created_at=now - timedelta(days=45),
        ))

        db.add(models.WorkerProfile(
            user_id=user_worker_julian.id,
            experience_level="senior",
            skills=["Machine Learning", "Python", "Ray", "Distributed Training", "CUDA"],
            portfolio_url="https://github.com/julianvance/llm-parallel",
            github_url="https://github.com/julianvance",
            phone="+1-415-555-0211",
            whatsapp_enabled=False,
            cloaked=True,
            weekly_availability_hours=35,
            percentile=94.2,
            created_at=now - timedelta(days=40),
        ))

        db.add(models.WorkerProfile(
            user_id=user_worker_rostova.id,
            experience_level="founding",
            skills=["ZK Proofs", "Wasm", "Rust", "Cryptography", "eBPF"],
            portfolio_url="https://github.com/erostova/wasm-zk-sandbox",
            github_url="https://github.com/erostova",
            phone="+1-415-555-0322",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=45,
            percentile=98.1,
            created_at=now - timedelta(days=35),
        ))

        # 4. Investor Profile
        db.add(models.InvestorProfile(
            user_id=user_investor.id,
            tier="Syndicate Tier 1",
            wallet_address="0x71C8821b0337E5652516A74C8215Ef72199B9901",
            preferred_sectors=["Enterprise AI", "Fintech Infrastructure", "Deep Tech", "Data Synthesis"],
            instant_alerts=True,
            weekly_digest=True,
            accreditation_status="verified",
            accreditation_expires_at=now + timedelta(days=365),
            created_at=now - timedelta(days=60),
        ))
        db.flush()

        # 5. Ventures
        ven_synthetix = models.Venture(
            id="ven_synthetix",
            founder_id=user_founder.id,
            cohort_id=cohort_alpha.id,
            name="Synthetix AI",
            thesis="Autonomous agentic simulation pipeline for multi-agent LLM systems in enterprise fintech.",
            sector="Enterprise AI & Fintech Stress-Testing",
            stage="Seed Stage ($500k SAFE)",
            clarity_score=96.4,
            constraints={"latencyMs": 15, "compliance": "SOC2/HIPAA", "squadSize": 4, "tps": 50000},
            raised_cents=50000000,   # $500,000
            runway_months=16,
            mrr_cents=850000,         # $8,500
            status="active",
            created_at=now - timedelta(days=60),
        )

        ven_polymatrix = models.Venture(
            id="ven_polymatrix",
            founder_id=user_founder_poly.id,
            cohort_id=cohort_alpha.id,
            name="PolyMatrix AI",
            thesis="High-throughput synthetic data engine for regulatory stress test suites.",
            sector="Data Synthesis & RegTech",
            stage="Seed Stage ($350k Raised)",
            clarity_score=92.1,
            constraints={"throughputMbs": 1200, "compliance": "GDPR/Basel-III"},
            raised_cents=35000000,
            runway_months=14,
            mrr_cents=620000,
            status="active",
            created_at=now - timedelta(days=50),
        )

        ven_chronodb = models.Venture(
            id="ven_chronodb",
            founder_id=user_founder_chrono.id,
            cohort_id=cohort_alpha.id,
            name="ChronoDB",
            thesis="Zero-copy temporal vector storage engine specifically engineered for multi-modal agent memory caches.",
            sector="High-Throughput Vector Storage",
            stage="Pre-Seed ($300k Raised)",
            clarity_score=91.0,
            constraints={"queryLatencyUs": 45, "zeroCopy": True},
            raised_cents=30000000,
            runway_months=12,
            mrr_cents=400000,
            status="active",
            created_at=now - timedelta(days=45),
        )

        ven_aether = models.Venture(
            id="ven_aether",
            founder_id=user_founder_aether.id,
            cohort_id=cohort_alpha.id,
            name="Aether Labs",
            thesis="Zero-knowledge verifiable agent runtime providing deterministic state sandboxing for enterprise workflows.",
            sector="Autonomous Agent Infrastructure",
            stage="Pre-Seed ($400k)",
            clarity_score=88.0,
            constraints={"zkProofSec": 1.2, "sandbox": "wasmtime"},
            raised_cents=40000000,
            runway_months=15,
            mrr_cents=250000,
            status="active",
            created_at=now - timedelta(days=40),
        )

        ven_kauri = models.Venture(
            id="ven_kauri",
            founder_id=user_founder_kauri.id,
            cohort_id=cohort_alpha.id,
            name="Kauri Health",
            thesis="Verifiable clinical reasoning agents with deterministic safety gates.",
            sector="BioTech & Health AI",
            stage="Pre-Seed ($75k Grant)",
            clarity_score=89.0,
            constraints={"fdaGate": True, "interpretability": "strict"},
            raised_cents=7500000,
            runway_months=12,
            mrr_cents=340000,
            status="active",
            created_at=now - timedelta(days=35),
        )

        db.add_all([ven_synthetix, ven_polymatrix, ven_chronodb, ven_aether, ven_kauri])
        db.flush()

        # 6. Squad Roles (Synthetix AI + others)
        role_synth_ceo = models.SquadRole(
            id="rol_synth_01",
            venture_id=ven_synthetix.id,
            title="Chief Executive Officer",
            description="Overall venture thesis, strategic enterprise partnerships, and capital allocation.",
            equity_pct=42.5,
            status="filled",
            filled_by_user_id=user_founder.id,
            requirements=["Executive Vision", "Enterprise Sales", "Domain Architecture"],
            created_at=now - timedelta(days=60),
        )

        role_synth_cto = models.SquadRole(
            id="rol_synth_02",
            venture_id=ven_synthetix.id,
            title="Chief Technology Officer",
            description="Core multi-agent coordination system, LLM inference topology, and technical roadmap.",
            equity_pct=32.0,
            status="filled",
            filled_by_user_id=user_cto.id,
            requirements=["Distributed Consensus", "C++ / Rust", "LLM Inference"],
            created_at=now - timedelta(days=60),
        )

        role_synth_growth = models.SquadRole(
            id="rol_synth_03",
            venture_id=ven_synthetix.id,
            title="Head of Enterprise Growth",
            description="Enterprise bank pilot acquisitions, regulatory liaison, and customer design partnerships.",
            equity_pct=10.5,
            status="filled",
            filled_by_user_id=user_growth.id,
            requirements=["Fintech Sales", "Pilot GTM", "Contract Negotiation"],
            created_at=now - timedelta(days=60),
        )

        role_synth_lead = models.SquadRole(
            id="rol_synth_04",
            venture_id=ven_synthetix.id,
            title="Lead Distributed Systems Architect",
            description="Low-latency MicroVM isolation framework, high-concurrency event loops, and soak test suites.",
            equity_pct=15.0,
            status="vacant",
            filled_by_user_id=None,
            requirements=["Rust or Go", "Distributed Consensus", "Low-Latency Networking"],
            created_at=now - timedelta(days=60),
        )

        role_poly_lead = models.SquadRole(
            id="rol_poly_01",
            venture_id=ven_polymatrix.id,
            title="High-Throughput Systems Core Engineer",
            description="Distributed state synchronization and synthetic banking compliance stress testing.",
            equity_pct=12.0,
            status="vacant",
            filled_by_user_id=None,
            requirements=["Distributed Systems", "Data Pipelines", "Python/Go"],
            created_at=now - timedelta(days=50),
        )

        role_chrono_lead = models.SquadRole(
            id="rol_chrono_01",
            venture_id=ven_chronodb.id,
            title="Storage Engine Lead Architect",
            description="Zero-copy temporal vector storage engine for LLM memory caches.",
            equity_pct=14.0,
            status="vacant",
            filled_by_user_id=None,
            requirements=["Rust Core", "Memory Layouts", "Zero-Copy IO"],
            created_at=now - timedelta(days=45),
        )

        role_aether_lead = models.SquadRole(
            id="rol_aether_01",
            venture_id=ven_aether.id,
            title="Wasm Sandbox Infrastructure Lead",
            description="Deterministic agent sandboxing and ZK state transition execution.",
            equity_pct=10.0,
            status="vacant",
            filled_by_user_id=None,
            requirements=["Wasmtime", "eBPF", "Rust"],
            created_at=now - timedelta(days=40),
        )

        db.add_all([role_synth_ceo, role_synth_cto, role_synth_growth, role_synth_lead, role_poly_lead, role_chrono_lead, role_aether_lead])
        db.flush()

        # 7. Cap Table (Section 6: sum(equity_pct) must equal 100.0)
        # 42.5 + 32.0 + 10.5 + 15.0 = 100.0
        db.add_all([
            models.CapTableEntry(
                id="cap_synth_01",
                venture_id=ven_synthetix.id,
                holder_user_id=user_founder.id,
                holder_label="Alex Mercer (CEO)",
                equity_pct=42.5,
                kind="founder",
                vested_pct=25.0,
                created_at=now - timedelta(days=60),
            ),
            models.CapTableEntry(
                id="cap_synth_02",
                venture_id=ven_synthetix.id,
                holder_user_id=user_cto.id,
                holder_label="Marcus Chen (CTO)",
                equity_pct=32.0,
                kind="cofounder",
                vested_pct=20.0,
                created_at=now - timedelta(days=60),
            ),
            models.CapTableEntry(
                id="cap_synth_03",
                venture_id=ven_synthetix.id,
                holder_user_id=user_growth.id,
                holder_label="Sarah Jenkins (Growth)",
                equity_pct=10.5,
                kind="cofounder",
                vested_pct=15.0,
                created_at=now - timedelta(days=60),
            ),
            models.CapTableEntry(
                id="cap_synth_04",
                venture_id=ven_synthetix.id,
                holder_user_id=None,
                holder_label="Open Founding Reserve / Option Pool",
                equity_pct=15.0,
                kind="option_pool",
                vested_pct=0.0,
                created_at=now - timedelta(days=60),
            ),
        ])
        db.flush()

        # 8. Matches (Section 6: Blind protocol uses candidate_code)
        db.add_all([
            models.Match(
                id="mat_synth_01",
                venture_id=ven_synthetix.id,
                role_id=role_synth_lead.id,
                worker_id=user_worker_elena.id,
                candidate_code="TX-5512B",
                synergy_score=98.0,
                fit_details={"skillsFit": 99.0, "latencyBonus": 97.0, "experienceMatch": "Strong Founding"},
                status="invited",
                created_at=now - timedelta(days=5),
            ),
            models.Match(
                id="mat_synth_02",
                venture_id=ven_synthetix.id,
                role_id=role_synth_lead.id,
                worker_id=user_worker_julian.id,
                candidate_code="TX-9042A",
                synergy_score=89.5,
                fit_details={"skillsFit": 88.0, "latencyBonus": 91.0, "experienceMatch": "Senior"},
                status="suggested",
                created_at=now - timedelta(days=4),
            ),
            models.Match(
                id="mat_synth_03",
                venture_id=ven_synthetix.id,
                role_id=role_synth_lead.id,
                worker_id=user_worker_rostova.id,
                candidate_code="TX-8821B",
                synergy_score=94.0,
                fit_details={"skillsFit": 95.0, "latencyBonus": 93.0, "experienceMatch": "Founding"},
                status="suggested",
                created_at=now - timedelta(days=3),
            ),
        ])
        db.flush()

        # 9. Challenges
        challenge_synth = models.Challenge(
            id="chl_synth_01",
            venture_id=ven_synthetix.id,
            role_id=role_synth_lead.id,
            title="Sprint #3: 50k TPS MicroVM Benchmark & GTM Stress Test",
            duration_hours=48,
            starts_at=now - timedelta(days=3),
            ends_at=now - timedelta(days=1),
            status="open",
            created_at=now - timedelta(days=4),
        )
        db.add(challenge_synth)
        db.flush()

        # 10. Submissions & Real Hashes (Section 6: Real SHA-256)
        sub_payload_elena = {
            "challenge_id": challenge_synth.id,
            "candidate_code": "TX-5512B",
            "score": 96.4,
            "p99_latency_ms": 1.42,
            "tests_passed": 48,
            "tests_total": 48,
        }
        sub_hash_elena = compute_hash(sub_payload_elena)

        sub_elena = models.Submission(
            id="sub_synth_01",
            challenge_id=challenge_synth.id,
            worker_id=user_worker_elena.id,
            candidate_code="TX-5512B",
            status="attested",
            score=96.4,
            p99_latency_ms=1.42,
            tests_passed=48,
            tests_total=48,
            hash=sub_hash_elena,
            replay_integrity=99.8,
            failure_recovery=98.5,
            concurrency_latency=96.0,
            code_elegance=94.5,
            reviewer_verdict="Exceptional zero-copy memory architecture. Passes all 48 latency & resilience test suites with zero degradation.",
            signed_at=now - timedelta(days=1),
            created_at=now - timedelta(days=2),
        )
        db.add(sub_elena)
        db.flush()

        # 11. Proof Reports
        proof_report_elena = models.ProofReport(
            id="prf_synth_01",
            worker_id=user_worker_elena.id,
            submission_id=sub_elena.id,
            sprint_name="Sprint #3: Distributed MicroVM Soak Test",
            completed_at=now - timedelta(days=1),
            score=96.4,
            cohort_rank=1,
            hash=sub_hash_elena,
            tests_passed=48,
            tests_total=48,
            p99_latency_ms=1.42,
            memory_leak_bytes=0,
            reviewer_verdict="Attested on-chain proof. Zero memory degradation under 50k TPS burst simulation.",
            created_at=now - timedelta(days=1),
        )
        db.add(proof_report_elena)
        db.flush()

        # 12. Invitations
        db.add_all([
            models.Invitation(
                id="inv_synth_01",
                venture_id=ven_synthetix.id,
                role_id=role_synth_lead.id,
                worker_id=user_worker_elena.id,
                equity_pct=15.0,
                terms="4-Year Vesting with 1-Year Cliff • Post-Money SAFE Protected",
                message="We reviewed your 50k TPS MicroVM benchmark submission and were blown away by your low-latency scheduler execution. We would love to have you as a founding team member to build out our high-throughput enterprise simulation stack.",
                status="pending",
                created_at=now - timedelta(hours=14),
            ),
            models.Invitation(
                id="inv_poly_01",
                venture_id=ven_polymatrix.id,
                role_id=role_poly_lead.id,
                worker_id=user_worker_elena.id,
                equity_pct=12.0,
                terms="Standard Founder Stock Agreement • Early Exercise Supported",
                message="Your background in distributed state synchronization fits perfectly with our continuous compliance simulation architecture.",
                status="pending",
                created_at=now - timedelta(days=1),
            ),
            models.Invitation(
                id="inv_chrono_01",
                venture_id=ven_chronodb.id,
                role_id=role_chrono_lead.id,
                worker_id=user_worker_elena.id,
                equity_pct=14.0,
                terms="Delaware C-Corp Cap Table Slot • Series Pre-Seed",
                message="We are building the fastest vector storage engine for LLMs. Your zero-copy memory benchmarks match our exact technical roadmap requirements.",
                status="pending",
                created_at=now - timedelta(days=2),
            ),
        ])
        db.flush()

        # 13. Applications
        db.add(models.Application(
            id="app_synth_01",
            role_id=role_synth_lead.id,
            worker_id=user_worker_elena.id,
            blind_token="BLIND-TOKEN-" + hashlib.sha256(b"TX-5512B-APPLY").hexdigest()[:16],
            status="reviewed",
            created_at=now - timedelta(days=3),
        ))
        db.flush()

        # 14. Transactions (from FounderFinancial.jsx)
        db.add_all([
            models.Transaction(
                id="txn_101",
                venture_id=ven_synthetix.id,
                occurred_on=now - timedelta(days=4),
                description="AWS Cloud MicroVM GPU Cluster Soak Test",
                category="infrastructure",
                amount_cents=-284000,
                proof_hash="0x8f9c21aa54b8e991204cf01284a1801c890123ef",
                created_at=now - timedelta(days=4),
            ),
            models.Transaction(
                id="txn_102",
                venture_id=ven_synthetix.id,
                occurred_on=now - timedelta(days=10),
                description="Enterprise Fintech Pilot Milestone Grant",
                category="revenue",
                amount_cents=1000000,
                proof_hash="0x3f7a8849921bcdef0123456789abcdef01234567",
                created_at=now - timedelta(days=10),
            ),
            models.Transaction(
                id="txn_103",
                venture_id=ven_synthetix.id,
                occurred_on=now - timedelta(days=18),
                description="Core Founding Squad Sprint #2 Stipends",
                category="payroll",
                amount_cents=-950000,
                proof_hash="0x12bb774088ac890123456789abcdef0123456789",
                created_at=now - timedelta(days=18),
            ),
            models.Transaction(
                id="txn_104",
                venture_id=ven_synthetix.id,
                occurred_on=now - timedelta(days=33),
                description="Delaware C-Corp Legal & IP Assignment Filing",
                category="legal",
                amount_cents=-145000,
                proof_hash="0x7e29bb10cc40890123456789abcdef0123456789",
                created_at=now - timedelta(days=33),
            ),
        ])
        db.flush()

        # 15. Financial Snapshots (6 Months)
        snapshots = [
            ("2025-05", 1200000, 300000, 29000000),
            ("2025-06", 1320000, 450000, 28130000),
            ("2025-07", 1400000, 550000, 27280000),
            ("2025-08", 1450000, 680000, 26510000),
            ("2025-09", 1480000, 750000, 25780000),
            ("2025-10", 1480000, 850000, 24250000),
        ]
        for idx, (m, burn, rev, cash) in enumerate(snapshots):
            db.add(models.FinancialSnapshot(
                id=f"snp_synth_{idx+1}",
                venture_id=ven_synthetix.id,
                month=m,
                burn_cents=burn,
                revenue_cents=rev,
                cash_cents=cash,
                created_at=now - timedelta(days=(6 - idx) * 30),
            ))
        db.flush()

        # 16. Funding Opportunities
        opp_syndicate = models.FundingOpportunity(
            id="opp_01",
            name="Fintech Infrastructure Angel Syndicate",
            category="syndicate",
            check_min_cents=5000000,   # $50k
            check_max_cents=25000000,  # $250k
            structure="Post-Money SAFE",
            tags=["Enterprise AI", "Fintech Infrastructure", "MicroVM"],
            timeline="2 Weeks",
            base_fit_pct=94.0,
            created_at=now - timedelta(days=20),
        )

        opp_vc = models.FundingOpportunity(
            id="opp_02",
            name="Deep Tech Velocity Micro-VC",
            category="micro_vc",
            check_min_cents=20000000,  # $200k
            check_max_cents=50000000,  # $500k
            structure="Priced Seed",
            tags=["AI Core", "Infrastructure", "High-Throughput"],
            timeline="4 Weeks",
            base_fit_pct=88.5,
            created_at=now - timedelta(days=20),
        )

        opp_grant = models.FundingOpportunity(
            id="opp_03",
            name="NSF Agentic Safety Research Grant",
            category="grant",
            check_min_cents=7500000,   # $75k
            check_max_cents=15000000,  # $150k
            structure="Non-Dilutive Grant",
            tags=["Safety", "Compliance", "Deterministic"],
            timeline="Immediate",
            base_fit_pct=91.0,
            created_at=now - timedelta(days=20),
        )

        db.add_all([opp_syndicate, opp_vc, opp_grant])
        db.flush()

        # 17. Funding Requests
        db.add(models.FundingRequest(
            id="fnr_01",
            venture_id=ven_synthetix.id,
            funding_opportunity_id=opp_syndicate.id,
            status="approved",
            created_at=now - timedelta(days=15),
        ))
        db.flush()

        # 18. Investments (from InvestorPortfolio.jsx)
        db.add_all([
            models.Investment(
                id="invst_synth_01",
                investor_id=user_investor.id,
                venture_id=ven_synthetix.id,
                instrument_type="safe",
                instrument_label="Post-Money SAFE",
                principal_cents=20000000,    # $200,000
                val_cap_cents=1000000000,   # $10,000,000
                discount_pct=20.0,
                equity_pct=2.0,
                contract_addr="0x38F01b22992B45Ac01a88091bc88",
                signed_on=now - timedelta(days=25),
                status="active",
                created_at=now - timedelta(days=25),
            ),
            models.Investment(
                id="invst_poly_01",
                investor_id=user_investor.id,
                venture_id=ven_polymatrix.id,
                instrument_type="safe",
                instrument_label="SAFE Note with MFN",
                principal_cents=15000000,    # $150,000
                val_cap_cents=800000000,    # $8,000,000
                discount_pct=20.0,
                equity_pct=1.875,
                contract_addr="0x49EA01771Ac01456bc99102844a",
                signed_on=now - timedelta(days=20),
                status="active",
                created_at=now - timedelta(days=20),
            ),
            models.Investment(
                id="invst_kauri_01",
                investor_id=user_investor.id,
                venture_id=ven_kauri.id,
                instrument_type="grant",
                instrument_label="Grant & Warrant",
                principal_cents=7500000,     # $75,000
                val_cap_cents=500000000,    # $5,000,000
                discount_pct=15.0,
                equity_pct=1.5,
                contract_addr="0x12A09c550C881a2430bc990142b",
                signed_on=now - timedelta(days=15),
                status="active",
                created_at=now - timedelta(days=15),
            ),
        ])
        db.flush()

        # 19. Milestone Updates
        milestone_01 = models.MilestoneUpdate(
            id="mls_synth_01",
            venture_id=ven_synthetix.id,
            headline="Sprint #3 Attested: 50,000 TPS MicroVM Stress Test Passed",
            body="Synthetix AI completed the autonomous agentic simulation pipeline benchmark. P99 latency measured at 1.42ms across all 48 test permutations with zero memory degradation.",
            stage_label="Phase 2 - Execution",
            tag="Engineering",
            merkle_proof="0x9a8f21bc44b201a45902bcde0123456789abcdef",
            deliverables=["Benchmark Suite", "Grafana Snapshot", "Attested Review Log"],
            metrics={"tps": 50000, "latencyP99Ms": 1.42, "testsPassed": 48},
            published_at=now - timedelta(days=1),
            created_at=now - timedelta(days=1),
        )
        db.add(milestone_01)
        db.flush()

        # 20. Milestone Reads
        db.add(models.MilestoneRead(
            investor_id=user_investor.id,
            update_id=milestone_01.id,
            read_at=now - timedelta(hours=6),
        ))

        # 21. Disclosure Requests
        db.add(models.DisclosureRequest(
            id="dsc_synth_01",
            investor_id=user_investor.id,
            venture_id=ven_synthetix.id,
            status="approved",
            created_at=now - timedelta(days=12),
        ))

        # 22. Notifications
        db.add_all([
            models.Notification(
                id="notif_01",
                user_id=user_founder.id,
                kind="sprint_attestation",
                body="Candidate TX-5512B completed Sprint #3 with 96.4/100 score.",
                read=False,
                created_at=now - timedelta(hours=15),
            ),
            models.Notification(
                id="notif_02",
                user_id=user_worker_elena.id,
                kind="invitation_received",
                body="Synthetix AI offered you the Lead Distributed Systems Architect role with 15.0% equity.",
                read=False,
                created_at=now - timedelta(hours=14),
            ),
            models.Notification(
                id="notif_03",
                user_id=user_investor.id,
                kind="milestone_published",
                body="Synthetix AI published Sprint #3 engineering milestone telemetry.",
                read=True,
                created_at=now - timedelta(hours=6),
            ),
        ])

        # 23. Audit Log (Section 6: Every state change writes audit_log)
        db.add_all([
            models.AuditLog(
                id="aud_01",
                actor_id=user_founder.id,
                action="INVITATION_CREATED",
                entity="invitations",
                entity_id="inv_synth_01",
                payload={"venture": "ven_synthetix", "role": "rol_synth_04", "candidate": "TX-5512B", "equity_pct": 15.0},
                created_at=now - timedelta(hours=14),
            ),
            models.AuditLog(
                id="aud_02",
                actor_id=user_founder.id,
                action="SUBMISSION_SCORED",
                entity="submissions",
                entity_id="sub_synth_01",
                payload={"score": 96.4, "status": "attested", "hash": sub_hash_elena},
                created_at=now - timedelta(days=1),
            ),
        ])

        db.commit()
        print("Demo database successfully seeded with all 24 models and demo cast!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
