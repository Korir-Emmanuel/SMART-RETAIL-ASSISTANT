def classify_intent(text):
    text = text.lower()
    supplier_keywords = [
        "supplier", "vendor", "price", "quote", "find", "who sells", 
        "where to buy", "who provides", "get from", "which supplier"
    ]
    dashboard_keywords = [
        "spending", "show", "visualize", "breakdown", "graph", "chart", "spend",
        "summarize", "overview", "grouped", "cost", "expenses", "trend", "visualization"
    ]

    if any(word in text for word in supplier_keywords):
        return "supplier_query"
    if any(word in text for word in dashboard_keywords):
        return "dashboard"
    return "unknown"
