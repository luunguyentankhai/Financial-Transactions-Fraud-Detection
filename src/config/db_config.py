import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="DB_Config", filename="DataBase")

load_dotenv()

@auto_logger(logger)
def db_engine():
    try:
        from google.colab import userdata
        db_url = userdata.get('DATABASE_URL')
        logger.info("Retrieved DATABASE_URL from Colab Secrets.")
    except ImportError: 
        load_dotenv()
        db_url = os.getenv("DATABASE_URL")
        logger.info("Retrieved DATABASE_URL from local .env file.")

    if not db_url:
        raise ValueError("DATABASE_URL is missing. Please check your .env file or Colab Secrets.")

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        logger.info("Automatically fixed connection dialect (postgres:// -> postgresql://).")

    engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5
                }
            )
    
    return engine
