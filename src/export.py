def to_excel(df, path):
    df.to_excel(path, index=False)


def to_csv(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")
