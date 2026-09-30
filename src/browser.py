from urllib.parse import urljoin

from . import config


def titles_with_browser(pages=1, proxy=None):
    """Собирает заголовки книг через браузерную автоматизацию (Playwright).

    Требует: pip install playwright && playwright install chromium
    """
    from playwright.sync_api import sync_playwright

    result = []
    with sync_playwright() as pw:
        launch_args = {"headless": True}
        if proxy:
            launch_args["proxy"] = {"server": proxy}
        browser = pw.chromium.launch(**launch_args)
        page = browser.new_page()
        page.goto(config.BASE_URL, timeout=30000)
        for _ in range(pages):
            page.wait_for_selector("article.product_pod")
            for link in page.query_selector_all("article.product_pod h3 a"):
                result.append(link.get_attribute("title"))
            next_link = page.query_selector("li.next a")
            if not next_link:
                break
            next_link.click()
            page.wait_for_load_state("networkidle")
        browser.close()
    return result
