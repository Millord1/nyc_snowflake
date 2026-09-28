import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import requests
import snowflake.connector
from dotenv import load_dotenv

from src.config.settings import DATA_DIR, Urls

load_dotenv()


class Ingestor:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.file_path: Path | None = None
        self.file_name: str | None = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_path and self.file_path.exists():
            self.file_path.unlink()
            print(f"Deleted {self.file_path}")

    def download_parquet(self, year: int, month: int) -> bool:
        self.data_dir.mkdir(exist_ok=True)

        self.file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
        self.file_path = self.data_dir / self.file_name

        tlc_url = Urls.get_trip_url(self.file_name)

        print(f"Downloading {tlc_url}", flush=True)

        response = requests.get(tlc_url, stream=True)

        if response.status_code in (403, 404):
            print(
                f"File not available: {self.file_name}. Stopping ingestion.",
                flush=True,
            )
            return False

        response.raise_for_status()

        with self.file_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded {self.file_path}", flush=True)

        return True

    def validate_with_duckdb(self) -> None:
        print(f"Validating {self.file_path} with DuckDB...")

        result = duckdb.sql(
            f"""
            SELECT
                COUNT(*) AS row_count,
                MIN(tpep_pickup_datetime) AS min_date,
                MAX(tpep_pickup_datetime) AS max_date
            FROM '{self.file_path}'
            """
        )

        print(result)

    @contextmanager
    def _get_snowflake_cnx(self):
        connection = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            warehouse=os.environ.get(
                "SNOWFLAKE_WAREHOUSE",
                "COMPUTE_WH",
            ),
            database=os.environ.get(
                "SNOWFLAKE_DATABASE",
                "NYC_TAXI",
            ),
            schema=os.environ.get(
                "SNOWFLAKE_SCHEMA",
                "RAW",
            ),
        )

        try:
            yield connection
        finally:
            connection.close()

    def upload_to_snowflake(self) -> None:
        print(f"Uploading {self.file_path} to Snowflake...")

        with self._get_snowflake_cnx() as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"""
                PUT 'file://{self.file_path.resolve()}'
                @NYC_TAXI.RAW.TLC_STAGE
                AUTO_COMPRESS=FALSE
                """
            )

            print("Uploaded to Snowflake stage")

    def copy_into_raw(self) -> None:
        print("Loading data into RAW...")

        with self._get_snowflake_cnx() as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"""
                COPY INTO NYC_TAXI.RAW.YELLOW_TAXI
                FROM @NYC_TAXI.RAW.TLC_STAGE/{self.file_name}
                FILE_FORMAT = (
                    FORMAT_NAME = 'NYC_TAXI.RAW.PARQUET_FORMAT'
                )
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
                """
            )

            for row in cursor.fetchall():
                print(row)

    @staticmethod
    def get_previous_month() -> tuple[int, int]:
        current_date = datetime.now()
        previous_month = current_date.replace(day=1) - timedelta(days=1)

        return previous_month.year, previous_month.month


if __name__ == "__main__":
    year, month = Ingestor.get_previous_month()

    with Ingestor() as ingestor:
        ingestor.download_parquet(year, month)
        ingestor.validate_with_duckdb()
        ingestor.upload_to_snowflake()
        ingestor.copy_into_raw()
