import os
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import requests
import snowflake.connector
from dotenv import load_dotenv

from src.config.settings import Urls

load_dotenv()

DATA_DIR = Path("data")


@contextmanager
def temporary_parquet(file_path: Path) -> Generator[Path]:
    try:
        yield file_path
    finally:
        if file_path.exists():
            file_path.unlink()
            print(f"Deleted {file_path}")


def download_parquet(year: int, month: int) -> Path:
    DATA_DIR.mkdir(exist_ok=True)

    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    file_path = DATA_DIR / file_name

    tlc_url = Urls.get_trip_url(file_name)

    print(f"Downloading {tlc_url}")

    response = requests.get(tlc_url, stream=True)
    response.raise_for_status()

    with file_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    print(f"Downloaded {file_path}")

    return file_path


def validate_with_duckdb(file_path: Path) -> None:
    print(f"Validating {file_path} with DuckDB...")

    result = duckdb.sql(
        f"""
        SELECT
            COUNT(*) AS row_count,
            MIN(tpep_pickup_datetime) AS min_date,
            MAX(tpep_pickup_datetime) AS max_date
        FROM '{file_path}'
        """
    )

    print(result)


def upload_to_snowflake(file_path: Path) -> None:
    print(f"Uploading {file_path} to Snowflake...")

    connection = snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
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
        cursor = connection.cursor()

        cursor.execute(
            f"""
            PUT 'file://{file_path.resolve()}'
            @NYC_TAXI.RAW.TLC_STAGE
            AUTO_COMPRESS=FALSE
            """
        )

        print("Uploaded to Snowflake stage")

    finally:
        connection.close()


def copy_into_raw(file_path: Path) -> None:
    print("Loading data into RAW...")

    connection = snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "NYC_TAXI"),
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "RAW"),
    )

    try:
        cursor = connection.cursor()

        file_name = file_path.name

        cursor.execute(
            f"""
            COPY INTO NYC_TAXI.RAW.YELLOW_TAXI
            FROM @NYC_TAXI.RAW.TLC_STAGE/{file_name}
            FILE_FORMAT = (
                FORMAT_NAME = 'NYC_TAXI.RAW.PARQUET_FORMAT'
            )
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            """
        )

        for row in cursor.fetchall():
            print(row)

    finally:
        connection.close()


def get_previous_month() -> tuple[int, int]:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.year, previous_month.month
