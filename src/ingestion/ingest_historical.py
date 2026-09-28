from src.config.settings import END_MONTH, START_MONTH, YEAR
from src.ingestion.ingestion import (
    download_parquet,
    temporary_parquet,
    upload_to_snowflake,
    validate_with_duckdb,
)


def main() -> None:
    for month in range(START_MONTH, END_MONTH + 1):
        print(f"Processing {YEAR}-{month:02d}")

        file_path = download_parquet(YEAR, month)

        with temporary_parquet(file_path):
            validate_with_duckdb(file_path)
            upload_to_snowflake(file_path)


if __name__ == "__main__":
    main()
