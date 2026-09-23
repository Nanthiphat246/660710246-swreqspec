"""Migration 001: create initial tables for booking feature.

รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

import importlib
import importlib.util
import os
from sqlalchemy import inspect

# Try package import first; fall back to loading models.py by path when running as script
try:
    from backend.db.models import Base
except Exception:
    models_path = os.path.join(os.path.dirname(__file__), "..", "models.py")
    models_path = os.path.normpath(models_path)
    spec = importlib.util.spec_from_file_location("backend.db.models", models_path)
    models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models)
    Base = models.Base


def upgrade(engine: Engine) -> None:
    """Create all tables for booking feature.

    รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # simple local check: create in-memory SQLite and run upgrade
    engine = create_engine("sqlite:///:memory:")
    upgrade(engine)
    # print created table names via SQLAlchemy inspector
    try:
        tables = inspect(engine).get_table_names()
    except Exception:
        tables = list(Base.metadata.tables.keys())
    print("Created tables:", tables)
