from src.config.settings import (
    END_MONTH,
    END_YEAR,
    START_MONTH,
    START_YEAR,
)
from src.ingestion.ingestion import Ingestor


def main() -> None:
    current_year = START_YEAR
    current_month = START_MONTH

    while (current_year, current_month) <= (END_YEAR, END_MONTH):
        print(
            f"Processing {current_year}-{current_month:02d}",
            flush=True,
        )

        with Ingestor() as ingestor:
            ingestor.download_parquet(current_year, current_month)
            ingestor.validate_with_duckdb()
            ingestor.upload_to_snowflake()
            ingestor.copy_into_raw()

        if current_month == 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1


if __name__ == "__main__":
    main()
