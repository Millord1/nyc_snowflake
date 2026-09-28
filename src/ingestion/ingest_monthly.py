from src.config.settings import YEAR
from src.ingestion.ingestion import Ingestor


def main() -> None:
    year = YEAR
    month = 6
    # year, month = get_previous_month()

    print(f"Processing {year}-{month:02d}")

    with Ingestor() as ingestor:
        ingestor.download_parquet(YEAR, month)
        ingestor.validate_with_duckdb()
        ingestor.upload_to_snowflake()
        ingestor.copy_into_raw()


if __name__ == "__main__":
    main()
