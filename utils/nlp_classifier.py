from textblob import TextBlob
import re

def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

def classify_intent(text):
    corrected_text = correct_spelling(text.lower())

    supplier_keywords = [
        "supplier", "vendor", "price", "quote", "find", "sells", 
        "buy", "provides", "supply", "supplied", "deliver", "procure", 
        "order", "seller", "provider", "purchase", "offer", "get"
    ]

    dashboard_keywords = [
        "spending", "show", "visualize", "breakdown", "graph", "chart", "spend", "summary",
        "summarize", "overview", "grouped", "cost", "expenses", "trend", "visualization"
    ]

    words = re.findall(r"\b\w+\b", corrected_text)

    supplier_match = any(word in supplier_keywords for word in words)
    dashboard_match = any(word in dashboard_keywords for word in words)

    if supplier_match:
        return "supplier_query", corrected_text
    elif dashboard_match:
        return "dashboard", corrected_text
    else:
        return "unknown", corrected_text
