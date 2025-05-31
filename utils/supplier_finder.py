import pandas as pd
def find_suppliers(text, df):
    user_words = text.lower().split()

    def match_row(desc):
        desc = str(desc).lower()
        return any(word in desc for word in user_words)

    matches = df[df["Item Description"].apply(match_row)]

    return matches[["Supplier/Vendor", "Unit Price", "Item Description"]].drop_duplicates()
