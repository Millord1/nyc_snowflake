import os
from pathlib import Path

import duckdb
import requests
import snowflake.connector

DATA_DIR = Path("data")


def download_parquet(year: int, month: int) -> Path:
    DATA_DIR.mkdir(exist_ok=True)

    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    file_path = DATA_DIR / file_name

    if file_path.exists():
        print(f"{file_path} already exists")
        return file_path

    tlc_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"

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
        cursor = connection.cursor()

        cursor.execute(
            f"""
            PUT 'file://{file_path.resolve()}'
            @NYC_TAXI.RAW.TLC_STAGE
            AUTO_COMPRESS=FALSE
            OVERWRITE=TRUE
            """
        )

        print("Uploaded to Snowflake stage")

    finally:
        connection.close()
