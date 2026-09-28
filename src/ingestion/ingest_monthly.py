from datetime import datetime, timedelta

from src.ingestion.ingestion import (
    download_parquet,
    upload_to_snowflake,
    validate_with_duckdb,
)


def get_previous_month() -> tuple[int, int]:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.year, previous_month.month


def main() -> None:
    year, month = get_previous_month()
    print(f"Processing {year}-{month:02d}")

    file_path = download_parquet(year, month)
    validate_with_duckdb(file_path)
    upload_to_snowflake(file_path)


if __name__ == "__main__":
    main()
