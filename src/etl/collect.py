import os

import kagglehub as kg
from pathlib import Path
import pandas as pd
from src.config import dir_config
from src.config.logs_config import setup_log, auto_logger
import stat
import shutil

from src.utils.file_helpers import conversion_file

logger = setup_log(name="Pull_data", filename="data")


class Data_Collection:
    @auto_logger(logger)
    def Collection(self):
        try:
            Path_Install = dir_config.Raw_Dir

            Cache_path = Path(
                kg.dataset_download(
                    "dangleee/nigerian-financial-transactions-fraud-detection"
                )
            )
            logger.info("Pulling data completed")

            for csv_file in Cache_path.rglob("*.csv"):
                target = Path_Install / "Data.csv"

                if target.exists():
                    target.chmod(target.stat().st_mode | stat.S_IWRITE)

                shutil.copy(csv_file, target)

                logger.info("Starting conversion .csv to .parquet")

                output = conversion_file(target, Path_Install / "Data.parquet")

                logger.info(f"Save file add {output}")
                os.remove(target)

        except Exception as e:
            logger.error(f"Error : {e}")
        finally:
            pass
