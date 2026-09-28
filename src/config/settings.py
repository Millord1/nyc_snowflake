from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path


class Urls(StrEnum):
    TRIP_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"

    @classmethod
    def get_trip_url(cls, filename: str) -> str:
        return cls.TRIP_URL + filename


DATA_DIR = Path("data")

START_YEAR = 2025
START_MONTH = 1

CURRENT_YEAR = datetime.now().year

END_DATE = datetime.now().replace(day=1) - timedelta(days=1)
END_YEAR = END_DATE.year
END_MONTH = END_DATE.month
