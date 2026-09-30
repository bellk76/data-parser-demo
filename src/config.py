import os

import requests

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "data-parser-demo/1.0 (+https://github.com/bellk76)"
REQUEST_DELAY = 0.2


def get_proxies():
    http = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    https = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    proxies = {}
    if http:
        proxies["http"] = http
    if https:
        proxies["https"] = https
    return proxies or None


def get_session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    proxies = get_proxies()
    if proxies:
        session.proxies.update(proxies)
    return session
