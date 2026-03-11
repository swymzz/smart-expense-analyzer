def categorize_transactions(df):

    categories = []

    for desc in df["description"].str.lower():

        if "uber" in desc or "ola" in desc:
            categories.append("Transport")

        elif "amazon" in desc or "flipkart" in desc:
            categories.append("Shopping")

        elif "swiggy" in desc or "zomato" in desc:
            categories.append("Food")

        elif "rent" in desc:
            categories.append("Housing")

        elif "salary" in desc:
            categories.append("Income")

        else:
            categories.append("Other")

    df["category"] = categories

    return df