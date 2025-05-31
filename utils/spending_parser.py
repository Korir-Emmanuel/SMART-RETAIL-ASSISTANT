def parse_spending_query(text):
    text = text.lower()
    group_by = "Main category"  # Default

    if "manager" in text or "managers" in text:
        group_by = "Category Manager(s)"
    elif "month" in text or "year" in text:
        group_by = "Month"
    elif "department" in text or "departments" in text:
        group_by = "Department"
    elif "division" in text or "divisions" in text:
        group_by = "Division"
    elif "expenditure type" in text:
        group_by = "Expenditure Type"
    elif "closure" in text:
        group_by = "Closure Status"
    elif "location" in text:
        group_by = "Locale(Foreign or Local based Suppliers)"
    elif "ownership" in text:
        group_by ="Special Interest Group- Women or Youth Owned Suppliers"
    elif "currency" in text:
        group_by ="Currency"
    elif "type" in text:
        group_by ="Type"
    elif "organization" in text or "organisation" in text:
        group_by ="OU Name"
    # Month filtering
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    month_filter = next((m.title() for m in months if m in text), None)

    return group_by, month_filter
