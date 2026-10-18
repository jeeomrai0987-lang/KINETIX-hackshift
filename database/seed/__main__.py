import sys
import os
import importlib
import pkgutil
from pathlib import Path
from sqlalchemy import text
from database.session import engine, Base, SessionLocal, DATABASE_URL
from database import models  # Ensure all models are registered in Base.metadata


def create_tables_via_alembic():
    """Apply Alembic migrations up to head to create and track all tables."""
    alembic_ini_path = Path(__file__).resolve().parent.parent.parent / "alembic.ini"
    if alembic_ini_path.exists():
        try:
            from alembic.config import Config
            from alembic import command

            cfg = Config(str(alembic_ini_path))
            print("[seed] Creating tables through Alembic migration (upgrade head)...")
            command.upgrade(cfg, "head")
            return
        except Exception as e:
            print(f"[seed] Alembic upgrade notice ({e}), applying create_all fallback...")
    Base.metadata.create_all(bind=engine)


def run_seeders(reset: bool = False):
    if reset:
        print("[seed] Reset requested. Dropping all tables...")
        # For local SQLite file, clean removal ensures fresh migration state
        if DATABASE_URL.startswith("sqlite") and "./ventureforge.db" in DATABASE_URL:
            db_path = Path("./ventureforge.db")
            if db_path.exists():
                try:
                    engine.dispose()
                    os.remove(db_path)
                except Exception:
                    pass

        if DATABASE_URL.startswith("sqlite"):
            try:
                with engine.connect() as conn:
                    conn.execute(text("PRAGMA foreign_keys=OFF"))
                    conn.commit()
                Base.metadata.drop_all(bind=engine)
                with engine.connect() as conn:
                    conn.execute(text("PRAGMA foreign_keys=ON"))
                    conn.commit()
            except Exception:
                pass
        else:
            Base.metadata.drop_all(bind=engine)

        create_tables_via_alembic()
    else:
        create_tables_via_alembic()

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
