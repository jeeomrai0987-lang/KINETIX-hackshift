import sys
import subprocess
import unittest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.session import SessionLocal, engine
from database.models.worker_activity import Invitation, Submission, ProofReport, Application
from database.seed.seed_worker_activity import get_submission_payload, get_proof_report_payload
from database.seed.common import canonical_hash
from database.seed.cast import USR_WORKER_03, USR_WORKER_05, VEN_SYNTHETIX


class TestWorkerActivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Verify if tables and seed data exist; if not, run full seed
        db = SessionLocal()
        try:
            count = db.query(Invitation).count()
            if count >= 3:
                return
        except Exception:
            pass
        finally:
            db.close()
            engine.dispose()

        result = subprocess.run(
            [sys.executable, "-m", "database.seed", "--reset"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"database.seed --reset failed:\n{result.stderr}\n{result.stdout}")

    def setUp(self):
        self.db: Session = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_foreign_keys_resolve_after_seed(self):
        """Verify that all cross-table foreign key relationships resolve cleanly."""
        # 1. Invitations
        invitations = self.db.query(Invitation).all()
        self.assertGreaterEqual(len(invitations), 3, "Expected at least 3 pending invitations")
        for inv in invitations:
            self.assertIsNotNone(inv.venture, f"Invitation {inv.id} venture FK failed to resolve")
            self.assertEqual(inv.venture.id, inv.venture_id)
            self.assertIsNotNone(inv.role, f"Invitation {inv.id} role FK failed to resolve")
            self.assertEqual(inv.role.id, inv.role_id)
            self.assertIsNotNone(inv.worker, f"Invitation {inv.id} worker FK failed to resolve")
            self.assertEqual(inv.worker.id, inv.worker_id)
            self.assertIsInstance(inv.equity_pct, (int, float), "Equity percentage must be numeric")

        # 2. Submissions
        submissions = self.db.query(Submission).all()
        self.assertGreaterEqual(len(submissions), 3, "Expected at least 3 challenge submissions")
        for sub in submissions:
            self.assertIsNotNone(sub.challenge, f"Submission {sub.id} challenge FK failed to resolve")
            self.assertEqual(sub.challenge.id, sub.challenge_id)
            self.assertIsNotNone(sub.worker, f"Submission {sub.id} worker FK failed to resolve")
            self.assertEqual(sub.worker.id, sub.worker_id)

        # 3. Proof Reports
        proof_reports = self.db.query(ProofReport).all()
        self.assertGreaterEqual(len(proof_reports), 3, "Expected at least 3 proof reports")
        for pr in proof_reports:
            self.assertIsNotNone(pr.worker, f"Proof report {pr.id} worker FK failed to resolve")
            self.assertEqual(pr.worker.id, pr.worker_id)
            if pr.submission_id:
                self.assertIsNotNone(pr.submission, f"Proof report {pr.id} submission FK failed to resolve")
                self.assertEqual(pr.submission.id, pr.submission_id)

        # 4. Applications
        applications = self.db.query(Application).all()
        self.assertGreaterEqual(len(applications), 2, "Expected at least 2 applications")
        for app in applications:
            self.assertIsNotNone(app.role, f"Application {app.id} role FK failed to resolve")
            self.assertEqual(app.role.id, app.role_id)
            self.assertIsNotNone(app.worker, f"Application {app.id} worker FK failed to resolve")
            self.assertEqual(app.worker.id, app.worker_id)
            self.assertTrue(app.blind_token.startswith("BLIND-TOK-"))

    def test_unique_constraints_reject_duplicates(self):
        """Verify that unique constraints (role_id, worker_id) on invitations & applications reject duplicates."""
        # 1. Test duplicate invitation
        existing_inv = self.db.query(Invitation).first()
        self.assertIsNotNone(existing_inv)
        dup_inv = Invitation(
            id="inv_dup_test",
            venture_id=existing_inv.venture_id,
            role_id=existing_inv.role_id,
            worker_id=existing_inv.worker_id,
            equity_pct=10.0,
            terms="Duplicate test",
            message="Duplicate test",
            status="pending"
        )
        self.db.add(dup_inv)
        with self.assertRaises(IntegrityError):
            self.db.flush()
        self.db.rollback()

        # 2. Test duplicate application
        existing_app = self.db.query(Application).first()
        self.assertIsNotNone(existing_app)
        dup_app = Application(
            id="app_dup_test",
            role_id=existing_app.role_id,
            worker_id=existing_app.worker_id,
            blind_token="BLIND-TOK-DUP",
            status="submitted"
        )
        self.db.add(dup_app)
        with self.assertRaises(IntegrityError):
            self.db.flush()
        self.db.rollback()

    def test_seeded_hashes_recompute_equal(self):
        """Verify that all submission and proof report hashes match canonical_hash() over their scored payloads."""
        # 1. Submissions
        submissions = self.db.query(Submission).all()
        for sub in submissions:
            recomputed = canonical_hash(get_submission_payload(sub))
            self.assertEqual(
                sub.hash,
                recomputed,
                f"Submission {sub.id} hash mismatch! Expected {recomputed}, got {sub.hash}"
            )
            self.assertTrue(sub.hash.startswith("0x"), "Submission hash must begin with '0x'")
            self.assertEqual(len(sub.hash), 66, "SHA-256 hash with '0x' prefix must be 66 characters")

        # 2. Proof Reports
        proof_reports = self.db.query(ProofReport).all()
        for pr in proof_reports:
            recomputed = canonical_hash(get_proof_report_payload(pr))
            self.assertEqual(
                pr.hash,
                recomputed,
                f"Proof report {pr.id} hash mismatch! Expected {recomputed}, got {pr.hash}"
            )
            self.assertTrue(pr.hash.startswith("0x"), "Proof report hash must begin with '0x'")
            self.assertEqual(len(pr.hash), 66, "SHA-256 hash with '0x' prefix must be 66 characters")


if __name__ == "__main__":
    unittest.main()
