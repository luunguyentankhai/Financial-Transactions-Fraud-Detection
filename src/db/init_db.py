from sqlalchemy import text, exc
from src.config.dir_config import sql_dir
from src.config.db_config import db_engine
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="DB_init", filename="DataBase")


@auto_logger(logger)
def run_schema_init():
    engine = db_engine()
    schema_path = sql_dir / "schema.sql"

    logger.info("Checking schema.sql file and initializing database structure...")

    if not schema_path.exists():
        raise FileNotFoundError(f"Not found file schema.sql at {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(schema_sql))

    logger.info("Structure ready. Database schema initialized successfully.")
    return True
