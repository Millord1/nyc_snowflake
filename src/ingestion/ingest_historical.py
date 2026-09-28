from src.ingestion.ingestion import (
    download_parquet,
    upload_to_snowflake,
    validate_with_duckdb,
)

YEAR = 2026
START_MONTH = 1
END_MONTH = 8


def main() -> None:
    for month in range(START_MONTH, END_MONTH + 1):
        print(f"Processing {YEAR}-{month:02d}")

        file_path = download_parquet(YEAR, month)
        validate_with_duckdb(file_path)
        upload_to_snowflake(file_path)


if __name__ == "__main__":
    main()
