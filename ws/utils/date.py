from datetime import datetime

GMT_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


def parse_datetime_to_gmt_format_str(time: datetime) -> str:
    return datetime.strftime(time, GMT_DATETIME_FORMAT)


def parse_gmt_format_str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, GMT_DATETIME_FORMAT)
