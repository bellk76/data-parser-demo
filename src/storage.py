import sqlite3

import pandas as pd


def save_sqlite(df, db_path, table="books"):
    connection = sqlite3.connect(db_path)
    df.to_sql(table, connection, if_exists="replace", index=False)
    connection.close()


def report(db_path, table="books"):
    connection = sqlite3.connect(db_path)
    by_rating = pd.read_sql_query(
        f"SELECT rating, COUNT(*) AS books, ROUND(AVG(price), 2) AS avg_price "
        f"FROM {table} GROUP BY rating ORDER BY rating DESC",
        connection,
    )
    by_category = pd.read_sql_query(
        f"SELECT category, COUNT(*) AS books, ROUND(AVG(price), 2) AS avg_price "
        f"FROM {table} WHERE category IS NOT NULL "
        f"GROUP BY category ORDER BY books DESC, avg_price DESC LIMIT 10",
        connection,
    )
    connection.close()
    return by_rating, by_category
