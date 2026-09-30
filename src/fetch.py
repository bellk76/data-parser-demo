import time

from . import config


def fetch(session, url, retries=3):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
            time.sleep(config.REQUEST_DELAY)
            return response.text
        except Exception as error:  # noqa: BLE001
            last_error = error
            time.sleep(config.REQUEST_DELAY * 2 * attempt)
    raise RuntimeError(f"Не удалось загрузить {url}: {last_error}")
