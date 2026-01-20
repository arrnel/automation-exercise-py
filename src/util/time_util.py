from datetime import datetime


def seconds_to_golang_duration_str(seconds: int) -> str:
    h = seconds / 3600
    m = (seconds - h * 3600) / 60
    s = seconds - (h * 3600 + m * 60)
    result = ""
    if h > 0:
        result += f"{h}h"
    if m > 0:
        result += f"{m}m"
    if s > 0:
        result += f"{s}s"
    return result


def next_year_unix_datetime() -> int:
    """Return next year unix datetime as int"""
    current_datetime = datetime.now()
    next_year_datetime = current_datetime.replace(year=current_datetime.year + 1)
    return int(next_year_datetime.timestamp())
