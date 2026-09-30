# data-parser-demo — сбор, очистка и выгрузка данных на Python

Демонстрационный инструмент автоматизации на **Python**: собирает данные с сайта,
очищает и преобразует их, сохраняет в **Excel/CSV** и **SQLite**, строит
**SQL-отчёты**. Поддерживает **прокси** и (опционально) **браузерную автоматизацию**.

Парсит учебный каталог книг [books.toscrape.com](https://books.toscrape.com/) —
сайт, созданный специально для практики парсинга.

## Что умеет

- **HTTP-парсинг** списка и карточек товаров (`requests` + `BeautifulSoup`, CSS-селекторы).
- Переход на **страницы товаров** и извлечение деталей (категория, UPC, цена, наличие).
- **Очистка и преобразование** данных: цена → `float`, рейтинг → `int`, наличие → `bool`, остаток → `int` (`pandas`).
- **Выгрузка**: `books.xlsx` (openpyxl), `books.csv`, база `books.db`.
- **SQL-отчёты**: группировки `GROUP BY`, `COUNT`, `AVG`, сортировки.
- **Прокси** через переменные окружения `HTTP_PROXY` / `HTTPS_PROXY`.
- **Браузерная автоматизация** (опционально, Playwright) — `src/browser.py`.
- **Тесты** на парсинг и очистку (`pytest`, без сети).

## Стек

Python 3 · requests · BeautifulSoup4 · lxml · pandas · openpyxl · SQLite · pytest · (Playwright — опционально)

## Быстрый старт

```bash
pip install -r requirements.txt
python -m src.parser_cli --pages 2
```

Результат: `data/books.xlsx`, `data/books.csv`, `data/books.db` + отчёты в консоли.

Пример вывода:

```
=== Отчёт по рейтингу (SQL GROUP BY) ===
 rating  books  avg_price
      5     10      31.65
      4      6      36.80
      ...

=== Топ категорий (SQL GROUP BY) ===
   category  books  avg_price
    Default      7      25.92
     Poetry      5      36.42
      ...
```

Параметры:
```
--pages N        сколько страниц каталога обойти (по умолчанию 2)
--out-dir DIR    куда сохранять (по умолчанию data)
--no-details     не заходить на страницы книг (быстро, только список)
```

## Прокси

```bash
# Windows PowerShell
$env:HTTPS_PROXY="http://user:pass@host:port"
python -m src.parser_cli --pages 1
```

## Браузерная автоматизация (опционально)

```bash
pip install playwright
playwright install chromium
python -c "from src.browser import titles_with_browser; print(len(titles_with_browser(pages=2)))"
```

## Тесты

```bash
python -m pytest -q
```

## Структура

```
├─ src/
│  ├─ config.py       настройки, сессия, прокси
│  ├─ fetch.py        HTTP-загрузка с ретраями
│  ├─ parse.py        разбор HTML (CSS-селекторы)
│  ├─ clean.py        очистка/преобразование (pandas)
│  ├─ storage.py      SQLite + SQL-отчёты
│  ├─ export.py       экспорт в Excel/CSV
│  ├─ browser.py      браузерная автоматизация (Playwright, опц.)
│  └─ parser_cli.py   точка входа (argparse)
├─ tests/
├─ requirements.txt
└─ README.md
```

## Примечания

- Это демонстрационный учебный проект; парсится сайт, предназначенный для практики.
- Данные (`data/`) не коммитятся — генерируются при запуске.
