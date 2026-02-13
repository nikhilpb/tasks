from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

REQUIRED_TABLES = {
    "users",
    "tasks",
    "task_dependencies",
    "tags",
    "task_tags",
    "calendar_sync",
    "notifications",
    "notification_settings",
}


def test_alembic_upgrade_creates_required_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "schema.db"
    database_url = f"sqlite:///{db_path}"

    project_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(alembic_cfg, "head")

    engine = create_engine(database_url)
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    assert REQUIRED_TABLES.issubset(table_names)
