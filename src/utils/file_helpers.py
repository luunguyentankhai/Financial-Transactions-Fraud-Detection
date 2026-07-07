from os.path import getsize

import matplotlib.pyplot as plt
from sqlalchemy import except_
from src.config.logs_config import setup_log, auto_logger
from pathlib import Path
import pandas as pd

logger = setup_log(name="File Helper", filename="utils")


@auto_logger(logger)
def show_img_exists(filepath, size):
    img = plt.imread(filepath)
    plt.figure(figsize=size)
    plt.imshow(img)
    plt.axis("off")
    plt.show()


@auto_logger(logger)
def is_cache(save_path, isredraw=True, size=(12, 10)) -> bool:
    if save_path.exists():
        logger.info(f"Img {save_path.name} has exist")
        if isredraw:
            logger.info(f"RELOAD IMAGE {save_path.name}")
            show_img_exists(save_path, size)
            return True
    return False


@auto_logger(logger)
def conversion_file(input_path, output_path):

    dtype_config = {
        # category
        "transaction_type": "category",
        "merchant_category": "category",
        "location": "category",
        "device_used": "category",
        "fraud_type": "category",
        "payment_channel": "category",
        "ip_address": "category",
        "sender_persona": "category",
        "user_top_category": "category",
        "ip_geo_region": "category",
        # string
        "transaction_id": "string",
        "device_hash": "string",
        # uint64
        "sender_account": "uint64",
        "receiver_account": "uint64",
        # uint8
        "is_fraud": "uint8",
        "velocity_score": "uint8",
        "bvn_linked": "uint8",
        "new_device_transaction": "uint8",
        "geospatial_velocity_anomaly": "uint8",
        "txn_hour": "uint8",
        "is_weekend": "uint8",
        "is_salary_week": "uint8",
        "is_night_txn": "uint8",
        "device_seen_count": "uint8",
        "is_device_shared": "uint8",
        "is_ip_shared": "uint8",
        "user_txn_count_total": "uint8",
        "user_txn_frequency_24h": "uint8",
        "txn_count_last_1h": "uint8",
        "txn_count_last_24h": "uint8",
        # uint16
        "ip_seen_count": "uint16",
        # float32
        "time_since_last_transaction": "float32",
        "spending_deviation_score": "float32",
        "geo_anomaly_score": "float32",
        "amount_ngn": "float32",
        "user_avg_txn_amt": "float32",
        "user_std_txn_amt": "float32",
        "total_amount_last_1h": "float32",
        "time_since_last": "float32",
        "avg_gap_between_txns": "float32",
        "merchant_fraud_rate": "float32",
        "channel_risk_score": "float32",
        "persona_fraud_risk": "float32",
        "location_fraud_risk": "float32",
    }

    try:
        logger.info("Load file .csv with optimal date types")
        df = pd.read_csv(input_path, dtype=dtype_config)

        logger.info("Compressing to file .parquet with zstd algorithm")
        df.to_parquet(output_path, engine="pyarrow", compression="zstd", index=False)
        if input_path.exists() and output_path.exists():
            old_size = getsize(input_path) / (1024 * 1024)
            new_size = getsize(output_path) / (1024 * 1024)
            logger.info(
                f"Conversion successful! Original size: {old_size:.2f} MB -> New size: {new_size:.2f} MB"
            )

        return output_path

    except Exception as e:
        logger.error(f"Error occurred during data conversion: {e}")
        raise
