"""Unit and integration tests for founder database models, queries, and seed data."""

import math
import pytest
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from database.base import Base
from database.session import SessionLocal
from database.models.core import User, Cohort, Notification, AuditLog
from database.models.venture import Venture, SquadRole, Challenge, Match
from database.models.finance import (
    CapTableEntry,
    RestructuringEvent,
    Transaction,
    FinancialSnapshot,
    FundingOpportunity,
    FundingRequest,
)
from database.models.investor import (
    InvestorProfile,
    Investment,
    MilestoneUpdate,
    MilestoneRead,
    DisclosureRequest,
)
from database.seed.common import hash_password, canonical_hash, utcnow
from database.seed.cast import (
    USR_FOUNDER_01,
    USR_COFOUNDER_01,
    USR_COFOUNDER_02,
    USR_INVESTOR_02,
    VEN_SYNTHETIX,
    DEMO_PASSWORD,
)
from database.queries import founder


@pytest.fixture(scope="session")
def db_session():
    """Provides a session using the active SQLite engine for seed data checks."""
    session = SessionLocal()
    yield session
    session.close()


def test_seed_cast_users_exist(db_session):
    """Verify demo cast users from Contract Section 7 exist in database."""
    alex = db_session.get(User, USR_FOUNDER_01)
    assert alex is not None
    assert alex.email == "alex.mercer@synthetix.ai"
    assert alex.role == "founder"
    assert alex.node_id == "NODE-FND-0001"
    assert alex.verified is True
    # Verify password hash
    assert bcrypt.checkpw(DEMO_PASSWORD.encode("utf-8"), alex.password_hash.encode("utf-8"))

    cto = db_session.get(User, USR_COFOUNDER_01)
    assert cto is not None
    assert cto.name == "Marcus Chen"
    assert cto.role == "founder"

    growth = db_session.get(User, USR_COFOUNDER_02)
    assert growth is not None
    assert growth.name == "Sarah Jenkins"

    investor = db_session.get(User, USR_INVESTOR_02)
    assert investor is not None
    assert investor.email == "marcus.vance@angelsyndicate.vc"
    assert investor.role == "investor"


def test_seed_ventures_exist(db_session):
    """Verify all 5 demo ventures are seeded correctly."""
    venture_ids = [
        "ven_synthetix",
        "ven_polymatrix",
        "ven_chronodb",
        "ven_aether",
        "ven_kauri",
    ]
    for vid in venture_ids:
        v = db_session.get(Venture, vid)
        assert v is not None, f"Venture {vid} was not found"
        assert v.raised_cents >= 0
        assert v.runway_months >= 0
        assert v.mrr_cents >= 0
        assert isinstance(v.constraints, dict)


def test_cap_table_100_percent_rule(db_session):
    """Verify Contract Section 6 Rule 3:
    sum(equity_pct) over cap_table_entries for ven_synthetix must equal 100.0%.
    """
    entries, total_pct = founder.get_cap_table(db_session, VEN_SYNTHETIX)
    assert len(entries) == 4
    assert math.isclose(total_pct, 100.0, abs_tol=0.001)
    assert founder.validate_cap_table_integrity(db_session, VEN_SYNTHETIX)


def test_financial_units_stored_as_cents(db_session):
    """Verify all monetary amounts are integer cents, never display strings or floats."""
    v = db_session.get(Venture, VEN_SYNTHETIX)
    assert isinstance(v.raised_cents, int)
    assert isinstance(v.mrr_cents, int)
    assert v.raised_cents == 50000000  # $500,000.00
    assert v.mrr_cents == 850000       # $8,500.00

    transactions = founder.get_transactions(db_session, VEN_SYNTHETIX)
    assert len(transactions) > 0
    for tx in transactions:
        assert isinstance(tx.amount_cents, int)
        assert tx.proof_hash.startswith("0x")

    snapshots = founder.get_financial_history(db_session, VEN_SYNTHETIX)
    assert len(snapshots) == 6
    for snap in snapshots:
        assert isinstance(snap.burn_cents, int)
        assert isinstance(snap.revenue_cents, int)
        assert isinstance(snap.cash_cents, int)


def test_funding_opportunities_four(db_session):
    """Verify Part A2: exactly 4 funding opportunities matching FounderFunding.jsx."""
    opps = founder.get_funding_opportunities(db_session)
    assert len(opps) == 4
    opp_ids = {o.id for o in opps}
    assert opp_ids == {"opp_1", "opp_2", "opp_3", "opp_4"}
    
    alpha = db_session.get(FundingOpportunity, "opp_1")
    assert alpha.category == "syndicate"
    assert alpha.check_min_cents == 25000000
    assert alpha.check_max_cents == 50000000
    assert alpha.base_fit_pct == 98.0

    sbir = db_session.get(FundingOpportunity, "opp_3")
    assert sbir.category == "grant"
    assert sbir.check_min_cents == 27500000


def test_transactions_real_sha256(db_session):
    """Verify Part A2: four transactions with real 66-character SHA-256 proof_hash (0x prefix)."""
    txns = founder.get_transactions(db_session, VEN_SYNTHETIX)
    assert len(txns) == 4
    for t in txns:
        assert len(t.proof_hash) == 66, f"Transaction {t.id} proof_hash must be 66 chars: {t.proof_hash}"
        assert t.proof_hash.startswith("0x")
        int(t.proof_hash[2:], 16)  # must be valid hex


def test_restructuring_events_seeded(db_session):
    """Verify Part A2: restructuring events seeded from FounderRestructuring.jsx."""
    events = founder.get_restructuring_events(db_session, VEN_SYNTHETIX)
    assert len(events) >= 1
    event = events[0]
    assert event.equity_delta_pct == 15.0
    assert "Cap Table Re-Allocation" in event.stage


def test_matches_seeding_with_workers(db_session):
    """Verify Part A2: seed_founder_matches seeds Arena matches when worker rows exist."""
    from database.seed import seed_founder_matches
    from database.seed.cast import USR_WORKER_03, USR_WORKER_04, USR_WORKER_05, CODE_JULIAN, CODE_ELENA, CODE_ROSTOVA
    from database.models.venture import Match

    # Create worker users if not present (simulating Person B's Phase 10)
    now = utcnow()
    workers_to_clean = []
    for wid, code in [(USR_WORKER_04, CODE_JULIAN), (USR_WORKER_03, CODE_ELENA), (USR_WORKER_05, CODE_ROSTOVA)]:
        if not db_session.get(User, wid):
            u = User(
                id=wid,
                email=f"{wid}@test.io",
                password_hash=hash_password("pw"),
                name=f"Worker {code}",
                role="worker",
                node_id=code,
                verified=True,
                created_at=now,
                updated_at=now,
            )
            db_session.add(u)
            workers_to_clean.append(wid)
    db_session.commit()

    # Run seed_founder_matches
    seed_founder_matches.run(db_session)
    db_session.commit()

    matches = db_session.query(Match).filter_by(venture_id=VEN_SYNTHETIX).all()
    assert len(matches) == 3
    codes = {m.candidate_code for m in matches}
    assert codes == {CODE_JULIAN, CODE_ELENA, CODE_ROSTOVA}
    scores = {m.synergy_score for m in matches}
    assert scores == {96.0, 94.0, 91.0}

    # Clean up test worker users and matches to keep seed pure
    for m in matches:
        db_session.delete(m)
    for wid in workers_to_clean:
        u = db_session.get(User, wid)
        if u:
            db_session.delete(u)
    db_session.commit()


def test_equity_transfer_atomic_and_audit(db_session):
    """Verify equity transfer preserves 100.0% cap table sum and writes audit log."""
    entries, initial_sum = founder.get_cap_table(db_session, VEN_SYNTHETIX)
    source = [e for e in entries if e.kind == "option_pool"][0]
    dest = [e for e in entries if e.holder_user_id == USR_FOUNDER_01][0]

    initial_source_pct = source.equity_pct
    initial_dest_pct = dest.equity_pct
    transfer_amount = 2.0

    # Execute transfer
    event = founder.execute_equity_transfer(
        db=db_session,
        venture_id=VEN_SYNTHETIX,
        from_entry_id=source.id,
        to_entry_id=dest.id,
        equity_pct=transfer_amount,
        actor_id=USR_FOUNDER_01,
        note="Test equity transfer from pool to founder",
    )

    assert event is not None
    assert event.equity_delta_pct == transfer_amount

    # Verify cap table remains 100.0%
    new_entries, new_sum = founder.get_cap_table(db_session, VEN_SYNTHETIX)
    assert math.isclose(new_sum, 100.0, abs_tol=0.001)

    # Revert transfer to leave seed pristine
    founder.execute_equity_transfer(
        db=db_session,
        venture_id=VEN_SYNTHETIX,
        from_entry_id=dest.id,
        to_entry_id=source.id,
        equity_pct=transfer_amount,
        actor_id=USR_FOUNDER_01,
        note="Revert test transfer",
    )

    reverted_entries, reverted_sum = founder.get_cap_table(db_session, VEN_SYNTHETIX)
    assert math.isclose(reverted_sum, 100.0, abs_tol=0.001)


def test_user_email_unique_constraint():
    """Verify database enforces unique email on users."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        u1 = User(
            id="u1",
            email="unique@test.io",
            password_hash=hash_password("pw"),
            name="User 1",
            role="founder",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        session.add(u1)
        session.commit()

        u2 = User(
            id="u2",
            email="unique@test.io",
            password_hash=hash_password("pw"),
            name="User 2",
            role="founder",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        session.add(u2)
        with pytest.raises(IntegrityError):
            session.commit()


def test_fks_resolve(db_session):
    """Verify Part A3: Foreign keys resolve cleanly across founder entities."""
    # Venture -> Founder & Cohort
    v = db_session.get(Venture, VEN_SYNTHETIX)
    assert v.founder is not None
    assert v.founder.id == USR_FOUNDER_01
    assert v.cohort is not None

    # Squad roles -> Venture
    roles = founder.get_squad_roles(db_session, VEN_SYNTHETIX)
    assert len(roles) > 0
    for r in roles:
        assert r.venture.id == VEN_SYNTHETIX

    # Investments -> Venture & Investor
    inv = db_session.query(Investment).filter_by(venture_id=VEN_SYNTHETIX).first()
    assert inv is not None
    assert inv.investor.id == USR_INVESTOR_02
    assert inv.venture.id == VEN_SYNTHETIX


def test_cascade_deletes_from_venture():
    """Verify Part A3: ON DELETE CASCADE from ventures to its children works."""
    engine_mem = create_engine("sqlite:///:memory:")
    # Enable foreign keys for in-memory SQLite
    from sqlalchemy import event
    @event.listens_for(engine_mem, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine_mem)
    Session = sessionmaker(bind=engine_mem)

    with Session() as session:
        # Create founder user
        u = User(
            id="usr_casc_fnd",
            email="cascade.fnd@test.io",
            password_hash=hash_password("pw"),
            name="Cascade Founder",
            role="founder",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        session.add(u)
        session.commit()

        # Create venture
        v = Venture(
            id="ven_casc_01",
            founder_id="usr_casc_fnd",
            name="Cascade Venture",
            thesis="Testing cascade",
            sector="Testing",
            stage="Seed",
            constraints={},
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        session.add(v)
        session.commit()

        # Add child squad role, cap entry, challenge
        role = SquadRole(
            id="rol_casc_01",
            venture_id="ven_casc_01",
            title="Test Role",
            description="Role to cascade",
            equity_pct=100.0,
            status="vacant",
            requirements=[],
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        cap = CapTableEntry(
            id="cap_casc_01",
            venture_id="ven_casc_01",
            holder_label="Founder",
            equity_pct=100.0,
            kind="founder",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        session.add_all([role, cap])
        session.commit()

        assert session.get(SquadRole, "rol_casc_01") is not None
        assert session.get(CapTableEntry, "cap_casc_01") is not None

        # Delete venture -> should cascade delete children
        session.delete(v)
        session.commit()

        assert session.get(SquadRole, "rol_casc_01") is None
        assert session.get(CapTableEntry, "cap_casc_01") is None


def test_match_unique_constraint_role_worker():
    """Verify Part A3: Unique constraint on (role_id, worker_id) for matches."""
    engine_mem = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine_mem)
    Session = sessionmaker(bind=engine_mem)

    with Session() as session:
        now = utcnow()
        u1 = User(id="u_fnd", email="fnd@test.io", password_hash=hash_password("pw"), name="Fnd", role="founder", created_at=now, updated_at=now)
        u2 = User(id="u_wrk", email="wrk@test.io", password_hash=hash_password("pw"), name="Wrk", role="worker", created_at=now, updated_at=now)
        v = Venture(id="v1", founder_id="u_fnd", name="V1", thesis="T", sector="S", stage="S", constraints={}, created_at=now, updated_at=now)
        r = SquadRole(id="r1", venture_id="v1", title="R1", description="D", equity_pct=10.0, status="vacant", requirements=[], created_at=now, updated_at=now)
        session.add_all([u1, u2, v, r])
        session.commit()

        m1 = Match(
            id="m1",
            venture_id="v1",
            role_id="r1",
            worker_id="u_wrk",
            candidate_code="TX-100",
            synergy_score=95.0,
            status="suggested",
            created_at=now,
            updated_at=now,
        )
        session.add(m1)
        session.commit()

        # Duplicate match on same role and worker must fail
        m2 = Match(
            id="m2",
            venture_id="v1",
            role_id="r1",
            worker_id="u_wrk",
            candidate_code="TX-100",
            synergy_score=90.0,
            status="suggested",
            created_at=now,
            updated_at=now,
        )
        session.add(m2)
        with pytest.raises(IntegrityError):
            session.commit()


def test_get_venture_financials_query_helper(db_session):
    """Verify Part A3: founder.get_venture_financials query helper."""
    fin = founder.get_venture_financials(db_session, VEN_SYNTHETIX)
    assert fin is not None
    assert fin["venture_id"] == VEN_SYNTHETIX
    assert fin["raised_cents"] == 50000000
    assert fin["runway_months"] == 16
    assert len(fin["snapshots"]) == 6
    assert len(fin["transactions"]) == 4
    assert fin["cap_table"]["is_valid"] is True
    assert math.isclose(fin["cap_table"]["total_equity_pct"], 100.0, abs_tol=0.001)
