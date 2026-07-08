import pandas as pd
import gc
from src.config.dir_config import Root_Data_File
from src.db.init_db import run_schema_init
from src.etl.cleaner import DataCleaner
from src.config.logs_config import setup_log, auto_logger
from src.db.db_manager import PostgresManager
from src.etl.collect import Data_Collection

logger = setup_log(name="Main_Pipeline", filename="data")


class DataPipeline:
    @auto_logger(logger)
    def Run_Pipeline(self):
        logger.info(f"Starting Pull and Push data (Two-Pass Architecture)")
        try:
            if not Root_Data_File.exists():
                logger.info(f"Data at doesn't have exists")
                Data_Collection().Collection()

            logger.info(f"Data at {Root_Data_File} have exists")
            # connect DB and create schema.sql
            run_schema_init()
            db_manager = PostgresManager()

            # Insert to DB Table
            cleaner = DataCleaner()

            # PASS 1 (Dimension Tables)
            cleaner.run_pass_1_dimensions(db_manager=db_manager)

            # PASS 2 (Fact Table)
            cleaner.run_pass_2_transactions(db_manager=db_manager)

            logger.info(f"PIPELINE SUCCESSFUL! All relations are strictly maintained.")

            del cleaner
            del db_manager
            gc.collect()
            logger.info("Garbage collection triggered. RAM freed successfully.")
        except Exception as e:
            logger.error(f"Pipeline Fail: {e}")
            raise
