from src.clean import clean_books, parse_price, parse_stock


def test_parse_price():
    assert parse_price("£51.77") == 51.77
    assert parse_price("£1,000.50") == 1000.50
    assert parse_price(None) is None


def test_parse_stock():
    assert parse_stock("In stock (22 available)") == 22
    assert parse_stock("") is None


def test_clean_books():
    rows = [
        {"title": "A", "price_raw": "£10.00", "rating": 3, "availability_raw": "In stock", "stock": "In stock (5 available)"},
        {"title": "B", "price_raw": "£5.50", "rating": 5, "availability_raw": "Out of stock", "stock": ""},
    ]
    df = clean_books(rows)
    assert set(["price", "in_stock", "stock_count"]).issubset(df.columns)
    assert list(df["rating"]) == [5, 3]
    assert df.iloc[0]["price"] == 5.5
    assert df.iloc[0]["in_stock"] is False or df.iloc[0]["in_stock"] is not True
