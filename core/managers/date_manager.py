import logging
from datetime import datetime

import pandas

LOGGER = logging.getLogger(__name__)


class DateManager:

    DEFAULT_TODAY_FORMAT = "%d-%m-%Y"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

    LIST_FORMAT = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y/%m/%dT%H:%M",
        "%d/%m/%Y",
        "%d/%m/%YT%H:%M",
        "%d/%m/%YT%H:%M:%S",
        "%d/%m/%YT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S",
        DEFAULT_DATETIME_FORMAT,
        DEFAULT_TODAY_FORMAT,
    ]

    @classmethod
    def generate_date_between_two_dates(cls, start_date, end_date):
        sdate = cls.string_to_date(start_date)
        edate = cls.string_to_date(end_date)
        date_ranges = pandas.date_range(sdate, edate, freq="d")
        return date_ranges.strftime(cls.DEFAULT_TODAY_FORMAT).to_list()

    @classmethod
    def string_to_datetime(cls, s):
        if not s:
            return None
        for fmt in cls.LIST_FORMAT:
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        LOGGER.warning(f"No valid datetime format found: input {s}")
        return None

    @classmethod
    def string_to_date(cls, s):
        if not s:
            return None
        for fmt in cls.LIST_FORMAT:
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                pass
        LOGGER.warning(f"No valid date format found: input {s}")
        return None

    @classmethod
    def get_today_to_string(cls, format=DEFAULT_TODAY_FORMAT):
        if format not in cls.LIST_FORMAT:
            LOGGER.warning(f"No valid date format found for format: {format}")
            return None
        try:
            return datetime.today().strftime(format)
        except TypeError:
            LOGGER.warning(
                f"No valid date format found for format: {format}, format have to be a string"
            )
            return None

    @classmethod
    def get_datetime_now_to_string(cls, format=DEFAULT_DATETIME_FORMAT):
        if format not in cls.LIST_FORMAT:
            LOGGER.warning(f"No valid date format found for format: {format}")
            return None
        try:
            return datetime.now().strftime(format)
        except TypeError:
            LOGGER.warning(
                f"No valid date format found for format: {format}, format have to be a string"
            )
            return None


if __name__ == "__main__":
    dates = DateManager.generate_date_between_two_dates(
        start_date="10-10-2022", end_date="23-10-2022"
    )
    print(dates)
