import datetime
import unittest
from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.models.core import User
from database.models.venture import Match, SquadRole
from database.models.worker_profile import WorkerProfile
from database.models.worker_activity import Invitation, Submission, Application, ProofReport
from database.seed.cast import USR_WORKER_03, USR_WORKER_04, USR_WORKER_05
from database.queries import worker as worker_queries


class TestWorkerIntegrity(unittest.TestCase):
    def setUp(self):
        self.db: Session = SessionLocal()

    def tearDown(self):
        self.db.rollback()
        self.db.close()

    def test_candidate_codes_are_unique_per_worker(self):
        """Verify candidate codes / node_ids are unique per worker candidate."""
        workers = self.db.query(User).filter(User.role == "worker").all()
        self.assertGreaterEqual(len(workers), 3, "Expected at least 3 seeded workers")

        node_ids = [w.node_id for w in workers if w.node_id]
        self.assertEqual(len(node_ids), len(set(node_ids)), f"Duplicate worker node_ids found: {node_ids}")

        # Check submissions: no candidate code is shared between two different workers
        submissions = self.db.query(Submission).all()
        candidate_code_to_worker = {}
        for sub in submissions:
            self.assertTrue(sub.candidate_code, f"Submission {sub.id} missing candidate_code")
            if sub.candidate_code in candidate_code_to_worker:
                self.assertEqual(
                    candidate_code_to_worker[sub.candidate_code],
                    sub.worker_id,
                    f"Candidate code '{sub.candidate_code}' is mapped to multiple distinct workers: "
                    f"{candidate_code_to_worker[sub.candidate_code]} and {sub.worker_id}"
                )
            else:
                candidate_code_to_worker[sub.candidate_code] = sub.worker_id

    def test_blind_protocol_data_check(self):
        """Verify that a worker's real name, email, and phone exist ONLY on users/worker_profiles,
        and are NEVER copied into matches, submissions, or applications."""
        workers = self.db.query(User).filter(User.role == "worker").all()
        profiles = self.db.query(WorkerProfile).all()
        profile_map = {p.user_id: p for p in profiles}

        real_identities = []
        for w in workers:
            prof = profile_map.get(w.id)
            phone = prof.phone if prof and prof.phone else None
            real_identities.append({
                "worker_id": w.id,
                "name": w.name,
                "email": w.email,
                "phone": phone
            })

        # 1. Submissions Check
        submissions = self.db.query(Submission).all()
        for sub in submissions:
            for ident in real_identities:
                name_parts = ident["name"].split()
                for part in name_parts:
                    if len(part) > 2:
                        self.assertNotIn(
                            part.lower(),
                            sub.candidate_code.lower(),
                            f"Blind Protocol Breach: Candidate code '{sub.candidate_code}' exposes worker name part '{part}'"
                        )
                self.assertNotIn(
                    ident["email"].lower(),
                    sub.candidate_code.lower(),
                    f"Blind Protocol Breach: Candidate code exposes email {ident['email']}"
                )
                if ident["phone"]:
                    clean_phone = ident["phone"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                    self.assertNotIn(
                        clean_phone,
                        sub.candidate_code,
                        f"Blind Protocol Breach: Candidate code exposes phone {ident['phone']}"
                    )

        # 2. Applications Check
        applications = self.db.query(Application).all()
        for app in applications:
            self.assertTrue(app.blind_token.startswith("BLIND-TOK-") or app.blind_token.startswith("TOK-BLIND-"))
            for ident in real_identities:
                name_parts = ident["name"].split()
                for part in name_parts:
                    if len(part) > 2:
                        self.assertNotIn(
                            part.lower(),
                            app.blind_token.lower(),
                            f"Blind Protocol Breach: Application blind_token '{app.blind_token}' exposes worker name part '{part}'"
                        )
                self.assertNotIn(
                    ident["email"].lower(),
                    app.blind_token.lower(),
                    f"Blind Protocol Breach: Application blind_token exposes email {ident['email']}"
                )

        # 3. Matches Check (Matches must store only IDs, never worker PII)
        matches = self.db.query(Match).all()
        for m in matches:
            # Check string attributes of Match
            match_dict = {c.name: getattr(m, c.name) for c in m.__table__.columns}
            for ident in real_identities:
                self.assertNotIn(ident["name"], match_dict.values(), "Match record contains worker name string")
                self.assertNotIn(ident["email"], match_dict.values(), "Match record contains worker email string")
                if ident["phone"]:
                    self.assertNotIn(ident["phone"], match_dict.values(), "Match record contains worker phone string")

    def test_accepted_invitations_have_responded_at_set(self):
        """Verify that accepted invitations have responded_at set, while pending invitations have None."""
        # 1. Existing seeded invitations should be pending with responded_at = None
        pending_invitations = self.db.query(Invitation).filter(Invitation.status == "pending").all()
        self.assertGreaterEqual(len(pending_invitations), 1, "Expected pending invitations")
        for inv in pending_invitations:
            self.assertIsNone(inv.responded_at, f"Pending invitation {inv.id} must have responded_at = None")

        # 2. Transitioning to accepted sets responded_at
        test_inv = pending_invitations[0]
        now = datetime.datetime.now(datetime.timezone.utc)
        test_inv.status = "accepted"
        test_inv.responded_at = now
        self.db.flush()

        reloaded = self.db.query(Invitation).filter(Invitation.id == test_inv.id).first()
        self.assertEqual(reloaded.status, "accepted")
        self.assertIsNotNone(reloaded.responded_at, "Accepted invitation must have responded_at populated")
        self.assertAlmostEqual(
            reloaded.responded_at.timestamp(),
            now.timestamp(),
            delta=5.0
        )

        # 3. Transitioning to declined also records responded_at
        if len(pending_invitations) > 1:
            decline_inv = pending_invitations[1]
            now_dec = datetime.datetime.now(datetime.timezone.utc)
            decline_inv.status = "declined"
            decline_inv.responded_at = now_dec
            self.db.flush()

            reloaded_dec = self.db.query(Invitation).filter(Invitation.id == decline_inv.id).first()
            self.assertEqual(reloaded_dec.status, "declined")
            self.assertIsNotNone(reloaded_dec.responded_at, "Declined invitation must have responded_at populated")

    def test_worker_queries_role_isolation(self):
        """Verify query helpers in queries/worker.py enforce strict worker_id isolation (Rule #4)."""
        # 1. Dashboard data
        dash_data = worker_queries.get_worker_dashboard_data(self.db, USR_WORKER_03)
        self.assertIsNotNone(dash_data)
        self.assertEqual(dash_data["worker_id"], USR_WORKER_03)
        self.assertIn("Top", dash_data["standing"])
        self.assertGreaterEqual(dash_data["pending_invitations_count"], 3)
        self.assertGreaterEqual(dash_data["total_proof_reports"], 3)

        # 2. List worker invitations scoped
        invites_03 = worker_queries.list_worker_invitations(self.db, USR_WORKER_03)
        self.assertGreaterEqual(len(invites_03), 3)
        for inv in invites_03:
            self.assertEqual(inv.worker_id, USR_WORKER_03)

        # Invitations for worker_04 should not leak worker_03's invitations
        invites_04 = worker_queries.list_worker_invitations(self.db, USR_WORKER_04)
        for inv in invites_04:
            self.assertEqual(inv.worker_id, USR_WORKER_04)

        # 3. Open opportunities
        opps = worker_queries.list_open_opportunities(self.db, USR_WORKER_03)
        self.assertGreaterEqual(len(opps), 1)
        for opp in opps:
            self.assertEqual(opp["status"], "vacant")
            self.assertIn("has_applied", opp)

        # 4. Proof of work scoping
        reports_03 = worker_queries.get_proof_of_work(self.db, USR_WORKER_03)
        self.assertGreaterEqual(len(reports_03), 3)
        for r in reports_03:
            self.assertEqual(r.worker_id, USR_WORKER_03)

        # Requesting another worker's proof report with a mismatched worker_id returns None
        target_report = reports_03[0]
        unauthorized_report = worker_queries.get_proof_of_work(self.db, USR_WORKER_04, report_id=target_report.id)
        self.assertIsNone(unauthorized_report, "Worker queries must not leak proof reports across workers")


if __name__ == "__main__":
    unittest.main()
