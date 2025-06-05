from textblob import TextBlob
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Define intent keywords globally so we can clean them out later
SUPPLIER_KEYWORDS = {
    "supplier", "vendor", "price", "quote", "find", "sells", 
    "buy", "provides", "supply", "supplied", "deliver", "procure", 
    "order", "seller", "provider", "purchase", "offer", "get"
}

DASHBOARD_KEYWORDS = {
    "spending", "show", "visualize", "breakdown", "graph", "chart", 
    "spend", "summary", "summarize", "overview", "grouped", "cost", 
    "expenses", "trend", "visualization"
}


def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())


def clean_and_tokenize(text):
    stopwords = ENGLISH_STOP_WORDS
    words = re.findall(r"\b\w+\b", text.lower())
    cleaned_words = [word for word in words if word not in stopwords]
    return cleaned_words


def classify_intent(text):
    corrected_text = correct_spelling(text.lower())
    cleaned_words = clean_and_tokenize(corrected_text)

    # Classify based on original words before intent keyword removal
    supplier_match = any(word in SUPPLIER_KEYWORDS for word in cleaned_words)
    dashboard_match = any(word in DASHBOARD_KEYWORDS for word in cleaned_words)

    # Remove intent keywords from cleaned_words
    filtered_words = [
        word for word in cleaned_words 
        if word not in SUPPLIER_KEYWORDS and word not in DASHBOARD_KEYWORDS
    ]

    if supplier_match:
        return "supplier_query", corrected_text, filtered_words
    elif dashboard_match:
        return "dashboard", corrected_text, filtered_words
    else:
        return "unknown", corrected_text, filtered_words
