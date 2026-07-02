import pandas as pd
import numpy as np
from src.config.logs_config import setup_log, auto_logger
from src.config.dir_config import Root_Data_File, Process_Dir

logger = setup_log(name="Data_Cleaner", filename="data")


class DataCleaner:
    def __init__(self, chunk_size=100000):
        self.chunk_size = chunk_size
        self.raw_path = Root_Data_File

    def _process_dimensions_chunk(self, df):
        # 1. Tách và gộp bảng Accounts (Gửi + Nhận)
        accounts_cols = [
            "sender_account",
            "bvn_linked",
            "sender_persona",
            "user_txn_count_total",
            "user_avg_txn_amt",
            "user_std_txn_amt",
            "user_txn_frequency_24h",
            "user_top_category",
            "persona_fraud_risk",
        ]
        # 1.1 Lấy dữ liệu thật của người gửi
        df_senders = (
            df[accounts_cols].copy().rename(columns={"sender_account": "account_id"})
        )

        # 1.2 Tạo dữ liệu giả (Dummy Data) cho người nhận
        df_receivers = pd.DataFrame()
        df_receivers["account_id"] = df["receiver_account"]
        df_receivers["bvn_linked"] = False
        df_receivers["sender_persona"] = "Unknown"
        df_receivers["user_txn_count_total"] = 0
        df_receivers["user_avg_txn_amt"] = 0.0
        df_receivers["user_std_txn_amt"] = 0.0
        df_receivers["user_txn_frequency_24h"] = 0
        df_receivers["user_top_category"] = "Unknown"
        df_receivers["persona_fraud_risk"] = 0.0

        # 1.3 Gộp chung và xóa trùng lặp (Ưu tiên giữ lại dữ liệu thật của sender nếu ID bị trùng)
        df_accounts = pd.concat([df_senders, df_receivers], ignore_index=True)
        df_accounts = df_accounts.drop_duplicates(subset=["account_id"], keep="first")

        # 2. Tách bảng Devices
        devices_cols = [
            "device_hash",
            "device_used",
            "device_seen_count",
            "is_device_shared",
        ]
        df_devices = df[devices_cols].copy().drop_duplicates(subset=["device_hash"])

        # 3. Tách bảng Locations
        locations_cols = [
            "ip_address",
            "location",
            "ip_geo_region",
            "ip_seen_count",
            "is_ip_shared",
            "location_fraud_risk",
        ]
        df_locations = df[locations_cols].copy().drop_duplicates(subset=["ip_address"])

        return df_accounts, df_devices, df_locations

    def _process_transactions_chunk(self, df):
        # 4. Tách bảng Transactions (chứa Khóa Ngoại và phần còn lại)
        transactions_cols = [
            "transaction_id",
            "timestamp",
            "sender_account",
            "receiver_account",
            "device_hash",
            "ip_address",
            "transaction_type",
            "payment_channel",
            "merchant_category",
            "amount_ngn",
            "is_fraud",
            "fraud_type",
            "time_since_last_transaction",
            "spending_deviation_score",
            "velocity_score",
            "geo_anomaly_score",
            "new_device_transaction",
            "geospatial_velocity_anomaly",
            "txn_hour",
            "is_weekend",
            "is_salary_week",
            "is_night_txn",
            "txn_count_last_1h",
            "txn_count_last_24h",
            "total_amount_last_1h",
            "time_since_last",
            "avg_gap_between_txns",
            "merchant_fraud_rate",
            "channel_risk_score",
        ]
        return df[transactions_cols].copy()

    @auto_logger(logger)
    def run_pass_1_dimensions(self, db_manager):
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw data file not found at: {self.raw_path}")

        logger.info(
            "PASS 1: Scanning data to extract and UPSERT Dimension tables (Accounts, Devices, Locations)..."
        )
        data_chunks = pd.read_csv(self.raw_path, chunksize=self.chunk_size)
        total_raw_rows = 0

        for i, chunk in enumerate(data_chunks):
            total_raw_rows += len(chunk)
            df_accounts, df_devices, df_locations = self._process_dimensions_chunk(
                chunk
            )

            db_manager.upsert(
                df_accounts, "accounts", "account_id", chunk_size=self.chunk_size
            )
            db_manager.upsert(
                df_devices, "devices", "device_hash", chunk_size=self.chunk_size
            )
            db_manager.upsert(
                df_locations, "locations", "ip_address", chunk_size=self.chunk_size
            )

        logger.info(
            f"PASS 1 FINISHED! Analyzed {total_raw_rows:,} rows and prepared all foreign keys."
        )
        return True

    @auto_logger(logger)
    def run_pass_2_transactions(self, db_manager):
        logger.info(
            "PASS 2: Scanning data again to BULK INSERT Fact table (Transactions)..."
        )
        data_chunks = pd.read_csv(self.raw_path, chunksize=self.chunk_size)
        total_raw_rows = 0

        for i, chunk in enumerate(data_chunks):
            total_raw_rows += len(chunk)
            df_transactions = self._process_transactions_chunk(chunk)
            db_manager.bulk_insert_chunk(df_transactions, "transactions")

            if (i + 1) % 5 == 0:  # Log tiến độ mỗi 5 chunk
                logger.info(
                    f"PASS 2: Inserted {total_raw_rows:,} transaction rows into DB..."
                )

        logger.info(
            f"PASS 2 FINISHED! Completely pushed {total_raw_rows:,} rows to Database."
        )
        return True


# LƯU Ý HỆ THỐNG:
# Phương pháp 2 Vòng (Two-pass) đã được áp dụng để giải quyết triệt để lỗi Foreign Key
# của receiver_account mà không cần xóa ràng buộc trong Database.
