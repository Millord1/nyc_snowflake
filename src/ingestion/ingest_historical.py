from src.config.settings import END_MONTH, START_MONTH, YEAR
from src.ingestion.ingestion import Ingestor


def main() -> None:
    for month in range(START_MONTH, END_MONTH + 1):
        print(f"Processing {YEAR}-{month:02d}")

        with Ingestor() as ingestor:
            ingestor.download_parquet(YEAR, month)
            ingestor.validate_with_duckdb()
            ingestor.upload_to_snowflake()
            ingestor.copy_into_raw()


if __name__ == "__main__":
    main()
