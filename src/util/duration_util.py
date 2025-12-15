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
