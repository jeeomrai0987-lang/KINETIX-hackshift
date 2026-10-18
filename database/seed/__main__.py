import sys
import importlib
import pkgutil
from pathlib import Path
from sqlalchemy import text
from database.session import engine, Base, SessionLocal, DATABASE_URL
from database import models  # Ensure all models are registered in Base.metadata

def run_seeders(reset: bool = False):
    if reset:
        print("[seed] Reset requested. Dropping all tables...")
        if DATABASE_URL.startswith("sqlite"):
            with engine.connect() as conn:
                conn.execute(text("PRAGMA foreign_keys=OFF"))
                conn.commit()
            Base.metadata.drop_all(bind=engine)
            with engine.connect() as conn:
                conn.execute(text("PRAGMA foreign_keys=ON"))
                conn.commit()
        else:
            Base.metadata.drop_all(bind=engine)

        print("[seed] Creating all tables fresh...")
        Base.metadata.create_all(bind=engine)
    else:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)

    # Auto-discover all seed modules in database/seed/ starting with seed_
    package_dir = Path(__file__).resolve().parent
    seed_modules = []

    for _, module_name, is_pkg in pkgutil.iter_modules([str(package_dir)]):
        if not is_pkg and module_name.startswith("seed_"):
            mod = importlib.import_module(f"database.seed.{module_name}")
            phase = getattr(mod, "PHASE", 100)
            seed_modules.append((phase, module_name, mod))

    # Sort strictly by (PHASE, filename)
    seed_modules.sort(key=lambda x: (x[0], x[1]))

    db = SessionLocal()
    try:
        for phase, name, mod in seed_modules:
            if hasattr(mod, "run"):
                print(f"[seed] Running {name} (Phase {phase})...")
                mod.run(db)
                db.commit()
        print("[seed] All seed phases executed successfully.")
    except Exception as e:
        db.rollback()
        print(f"[seed] Error executing seeders: {e}", file=sys.stderr)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    run_seeders(reset=reset_flag)
