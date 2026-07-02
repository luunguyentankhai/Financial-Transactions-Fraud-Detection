import csv
from io import StringIO
from sqlalchemy import text
from src.config.db_config import db_engine
from src.config.logs_config import setup_log, auto_logger

logger = setup_log(name="PostgresManager", filename="DataBase")


def psql_insert_copy(table, conn, keys, data_iter):
    """
    Hàm hỗ trợ ép dữ liệu vào DB siêu tốc (High-Performance Bulk Insert).
    Sử dụng lệnh COPY của PostgreSQL từ một vùng đệm RAM (StringIO).
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ", ".join('"{}"'.format(k) for k in keys)
        table_name = (
            "{}.{}".format(table.schema, table.name) if table.schema else table.name
        )

        sql = "COPY {} ({}) FROM STDIN WITH CSV".format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


class PostgresManager:
    def __init__(self):
        self.engine = db_engine()

    @auto_logger(logger)
    def bulk_insert_chunk(self, df, table_name):
        if df.empty:
            logger.warning(
                f"DataFrame is empty, skip bulk_insert for table {table_name}"
            )
            return
        with self.engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists="append",
                index=False,
                method=psql_insert_copy,
            )

    @auto_logger(logger)
    def upsert(self, df, table_name, pk_column, chunk_size=100000):
        if df.empty:
            logger.warning(f"DataFrame is empty, skip upsert for table {table_name}")
            return

        temp_table = f"stg_{table_name}"
        columns_list = [f"{col}" for col in df.columns]
        columns = ", ".join(columns_list)

        upsert_sql = text(f"""
                INSERT INTO {table_name} ({columns})
                SELECT {columns} FROM {temp_table}
                ON CONFLICT ({pk_column}) DO NOTHING;
            """)

        with self.engine.begin() as conn:
            # Dùng COPY đưa data vào bảng Staging (tạm thời) cực nhanh
            df.to_sql(
                name=temp_table,
                con=conn,
                if_exists="replace",
                index=False,
                chunksize=chunk_size,
                method=psql_insert_copy,
            )

            conn.execute(upsert_sql)
            conn.execute(text(f"DROP TABLE {temp_table}"))

        logger.info(f"Data push on {table_name} safe")

        with self.engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(
                text(f"VACUUM {table_name};")
            )

        logger.info(f"Running VACUUM clean table {table_name}")
