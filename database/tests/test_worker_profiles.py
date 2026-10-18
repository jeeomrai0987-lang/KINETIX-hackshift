import unittest
from sqlalchemy.orm import Session
from database.session import SessionLocal, engine
from database.base import Base
from database.models.core import User, Cohort
from database.models.worker_profile import WorkerProfile


class TestWorkerProfiles(unittest.TestCase):
    def setUp(self):
        self.db: Session = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_every_worker_has_exactly_one_profile(self):
        """Verify that every user with role 'worker' has exactly one 1:1 WorkerProfile."""
        workers = self.db.query(User).filter(User.role == "worker").all()
        self.assertGreater(len(workers), 0, "Expected at least one seeded worker user")

        for worker in workers:
            profile = self.db.query(WorkerProfile).filter(WorkerProfile.user_id == worker.id).all()
            self.assertEqual(
                len(profile),
                1,
                f"Worker {worker.id} ({worker.name}) must have exactly one profile, found {len(profile)}"
            )
            self.assertIsNotNone(worker.worker_profile)
            self.assertEqual(worker.worker_profile.user_id, worker.id)

    def test_cloaked_defaults_to_true(self):
        """Verify that cloaked defaults to True to maintain blind protocol integrity."""
        # 1. Check all seeded profiles
        profiles = self.db.query(WorkerProfile).all()
        self.assertGreater(len(profiles), 0)
        for p in profiles:
            self.assertTrue(p.cloaked, f"Profile for {p.user_id} should have cloaked=True")

        # 2. Check model column default
        new_profile = WorkerProfile(user_id="temp_user")
        self.assertTrue(new_profile.cloaked, "WorkerProfile.cloaked must default to True")

    def test_skills_are_lists_of_strings(self):
        """Verify that profile skills are stored as JSON lists of non-empty strings."""
        profiles = self.db.query(WorkerProfile).all()
        for p in profiles:
            self.assertIsInstance(
                p.skills,
                list,
                f"Worker {p.user_id} skills must be a list, got {type(p.skills)}"
            )
            self.assertGreater(
                len(p.skills),
                0,
                f"Worker {p.user_id} must have at least one skill"
            )
            for skill in p.skills:
                self.assertIsInstance(skill, str)
                self.assertTrue(len(skill.strip()) > 0)

    def test_experience_level_validity(self):
        """Verify that experience_level is one of the valid contract tiers."""
        valid_tiers = {"junior", "mid", "senior", "founding"}
        profiles = self.db.query(WorkerProfile).all()
        for p in profiles:
            self.assertIn(
                p.experience_level,
                valid_tiers,
                f"Worker {p.user_id} has invalid experience level: {p.experience_level}"
            )

    def test_weekly_availability_and_percentile(self):
        """Verify availability hours and percentile metrics are valid numeric ranges."""
        profiles = self.db.query(WorkerProfile).all()
        for p in profiles:
            self.assertGreater(p.weekly_availability_hours, 0)
            self.assertLessEqual(p.weekly_availability_hours, 168)
            self.assertGreaterEqual(p.percentile, 0.0)
            self.assertLessEqual(p.percentile, 100.0)


if __name__ == "__main__":
    unittest.main()
