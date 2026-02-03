import time
from collections.abc import Callable


def retry(
    action: Callable[[], bytes],
    retries: int,
    delay: float,
    error_factory: Callable[[Exception | None], Exception],
) -> bytes:
    last_exc = None

    for attempt in range(1, retries + 1):

        try:
            return action()
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(delay)

    raise error_factory(last_exc)
