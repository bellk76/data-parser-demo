from urllib.parse import urljoin

from bs4 import BeautifulSoup

RATING_BY_CLASS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def rating_to_int(class_attr):
    for name in class_attr or []:
        if name in RATING_BY_CLASS:
            return RATING_BY_CLASS[name]
    return 0


def parse_listing(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        title = link["title"].strip() if link and link.has_attr("title") else ""
        price = card.select_one("p.price_color")
        availability = card.select_one("p.instock.availability")
        rating = card.select_one("p.star-rating")
        books.append(
            {
                "title": title,
                "url": urljoin(base_url, link["href"]) if link else None,
                "price_raw": price.get_text(strip=True) if price else None,
                "rating": rating_to_int(rating.get("class") if rating else []),
                "availability_raw": availability.get_text(strip=True) if availability else "",
            }
        )
    return books


def parse_detail(html):
    soup = BeautifulSoup(html, "lxml")
    breadcrumbs = soup.select("ul.breadcrumb li a")
    category = breadcrumbs[-1].get_text(strip=True) if breadcrumbs else ""

    description = ""
    header = soup.select_one("#product_description")
    if header:
        paragraph = header.find_next_sibling("p")
        description = paragraph.get_text(strip=True) if paragraph else ""

    table = {
        row.th.get_text(strip=True): row.td.get_text(strip=True)
        for row in soup.select("table.table-striped tr")
        if row.th and row.td
    }
    return {
        "category": category,
        "description": description,
        "upc": table.get("UPC"),
        "price_excl_tax": table.get("Price (excl. tax)"),
        "price_incl_tax": table.get("Price (incl. tax)"),
        "stock": table.get("Availability"),
    }
