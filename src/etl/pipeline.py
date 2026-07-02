import pandas as pd
from src.config import dir_config
from src.db.init_db import run_schema_init
from src.etl.cleaner import DataCleaner
from src.config.logs_config import setup_log, auto_logger
from src.db.db_manager import PostgresManager

logger = setup_log(name="Main_Pipeline", filename="data")


class DataPipeline:
    @auto_logger(logger)
    def Run_Pipeline(self):
        logger.info(f"Starting Pull and Push data (Two-Pass Architecture)")
        try:
            run_schema_init()
            # 1. Khởi tạo kết nối DB
            db_manager = PostgresManager()

            # 2. Khởi tạo DataCleaner
            cleaner = DataCleaner()

            # 3. Kích hoạt luồng PASS 1 (Dimension Tables)
            cleaner.run_pass_1_dimensions(db_manager=db_manager)

            # 4. Kích hoạt luồng PASS 2 (Fact Table)
            cleaner.run_pass_2_transactions(db_manager=db_manager)

            logger.info(f"PIPELINE SUCCESSFUL! All relations are strictly maintained.")

        except Exception as e:
            logger.error(f"Pipeline Fail: {e}")
            raise
