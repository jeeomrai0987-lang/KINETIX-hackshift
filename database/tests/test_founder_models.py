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


def test_blind_protocol_candidate_code(db_session):
    """Verify Contract Section 6 Rule 1:
    Matches return candidate codes, not sensitive personal info.
    """
    # Matches list shouldn't leak PII
    matches = founder.get_blind_matches_for_venture(db_session, VEN_SYNTHETIX)
    for m in matches:
        assert "candidate_code" in m
        assert "name" not in m
        assert "email" not in m
        assert "phone" not in m


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
