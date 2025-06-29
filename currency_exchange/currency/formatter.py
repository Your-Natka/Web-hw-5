def format_result(date, data, currencies):
    result = {date: {}}
    for item in data.get("exchangeRate", []):
        if item.get("currency") in currencies:
            result[date][item["currency"]] = {
                "sale": item.get("saleRate", item.get("saleRateNB")),
                "purchase": item.get("purchaseRate", item.get("purchaseRateNB")),
            }
    return result
