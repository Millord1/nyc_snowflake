from src.config.settings import YEAR
from src.ingestion.ingestion import (
    copy_into_raw,
    download_parquet,
    temporary_parquet,
    upload_to_snowflake,
    validate_with_duckdb,
)


def main() -> None:
    year = YEAR
    month = 6
    # year, month = get_previous_month()

    print(f"Processing {year}-{month:02d}")

    file_path = download_parquet(year, month)

    with temporary_parquet(file_path):
        validate_with_duckdb(file_path)
        upload_to_snowflake(file_path)
        copy_into_raw(file_path)


if __name__ == "__main__":
    main()
