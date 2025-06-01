import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def clean_text(text):

    stopwords = ENGLISH_STOP_WORDS
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word not in stopwords]

def find_suppliers(text, df):
    user_words = clean_text(text)

    def match_row(desc):
        desc = str(desc).lower()
        return any(word in desc for word in user_words)

    matches = df[df["Item Description"].apply(match_row)]

    return matches[["Supplier/Vendor", "Unit Price", "Item Description"]].drop_duplicates()
