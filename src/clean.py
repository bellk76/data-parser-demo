import re

import pandas as pd


def parse_price(text):
    if not text:
        return None
    match = re.search(r"\d+(?:\.\d+)?", text.replace(",", ""))
    return float(match.group()) if match else None


def parse_stock(text):
    if not text:
        return None
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def clean_books(rows):
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["price"] = df["price_raw"].map(parse_price)
    df["in_stock"] = df["availability_raw"].str.contains("In stock", case=False, na=False)
    if "stock" in df.columns:
        df["stock_count"] = df["stock"].map(parse_stock)

    drop = [c for c in ("price_raw", "availability_raw") if c in df.columns]
    df = df.drop(columns=drop)
    df = df.sort_values(["rating", "price"], ascending=[False, False]).reset_index(drop=True)
    return df
