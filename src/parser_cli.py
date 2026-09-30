import argparse
import os
import sys
from urllib.parse import urljoin

from . import clean, config, export, fetch, parse, storage


def collect(pages, include_details=True):
    session = config.get_session()
    rows = []
    for page in range(1, pages + 1):
        url = urljoin(config.BASE_URL, f"catalogue/page-{page}.html")
        html = fetch.fetch(session, url)
        items = parse.parse_listing(html, url)
        for item in items:
            if include_details and item.get("url"):
                try:
                    detail_html = fetch.fetch(session, item["url"])
                    item.update(parse.parse_detail(detail_html))
                except Exception as error:  # noqa: BLE001
                    print(f"  ! деталь не загружена: {item['url']} ({error})", file=sys.stderr)
            rows.append(item)
        print(f"страница {page}: собрано {len(items)} книг", file=sys.stderr)
    return rows


def main():
    parser = argparse.ArgumentParser(description="Парсер каталога книг (демо автоматизации)")
    parser.add_argument("--pages", type=int, default=2, help="сколько страниц каталога обойти")
    parser.add_argument("--out-dir", default="data", help="куда сохранять результаты")
    parser.add_argument("--no-details", action="store_true", help="не заходить на страницы книг")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    rows = collect(args.pages, include_details=not args.no_details)
    df = clean.clean_books(rows)

    db_path = os.path.join(args.out_dir, "books.db")
    storage.save_sqlite(df, db_path)
    export.to_excel(df, os.path.join(args.out_dir, "books.xlsx"))
    export.to_csv(df, os.path.join(args.out_dir, "books.csv"))

    by_rating, by_category = storage.report(db_path)
    print("\n=== Отчёт по рейтингу (SQL GROUP BY) ===")
    print(by_rating.to_string(index=False))
    print("\n=== Топ категорий (SQL GROUP BY) ===")
    print(by_category.to_string(index=False))
    print(f"\nВсего книг: {len(df)}. Файлы: {args.out_dir}/books.{{xlsx,csv,db}}")


if __name__ == "__main__":
    main()
