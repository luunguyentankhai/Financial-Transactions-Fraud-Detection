import kagglehub as kg
from pathlib import Path
import pandas as pd
from src.config import dir_config
from src.config.logs_config import setup_log, auto_logger
import stat
import shutil

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

                logger.info(f"Drop trash column from {csv_file.name}")

                chunk_size = 100000
                first_chunk = True

                for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                    cols_to_drop = [
                        col for col in chunk.columns if col.lower() == "isflaggedfraud"
                    ]
                    if cols_to_drop:
                        chunk.drop(columns=cols_to_drop, inplace=True)

                    chunk.to_csv(
                        target,
                        mode="w" if first_chunk else "a",
                        header=first_chunk,
                        index=False,
                    )
                    first_chunk = False

                logger.info(f"Save file add {target}")
                target.chmod(target.stat().st_mode | stat.S_IWRITE)

        except Exception as e:
            logger.error(f"Error : {e}")
        finally:
            pass

if __name__ == "__main__":
    data= Data_Collection()
    data.Collection()