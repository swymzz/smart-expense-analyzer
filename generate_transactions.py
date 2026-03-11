import pandas as pd
import random
from datetime import datetime, timedelta

# merchants by category
food = ["Swiggy", "Zomato", "Cafe Coffee Day", "McDonalds", "Dominos"]
transport = ["Uber", "Ola", "Metro Recharge", "Rapido"]
shopping = ["Amazon", "Flipkart", "Myntra", "Ajio"]
entertainment = ["Netflix", "Spotify", "BookMyShow"]
bills = ["Electricity Bill", "Water Bill", "Internet Bill"]

normal_merchants = food + transport + shopping + entertainment + bills

# anomaly merchants
anomaly_merchants = [
    "Luxury Watch Store",
    "Crypto Exchange Transfer",
    "Foreign Currency Transaction",
    "International Flight Booking",
    "Unknown International Merchant",
    "High Value Electronics Purchase"
]

data = []

start_date = datetime(2026, 1, 1)

# generate normal transactions
for i in range(280):

    date = start_date + timedelta(days=random.randint(0, 60))

    merchant = random.choice(normal_merchants)

    if merchant in food:
        amount = random.randint(200, 800)

    elif merchant in transport:
        amount = random.randint(150, 500)

    elif merchant in shopping:
        amount = random.randint(1000, 5000)

    elif merchant in entertainment:
        amount = random.randint(150, 900)

    else:
        amount = random.randint(800, 4000)

    data.append({
        "date": date.strftime("%Y-%m-%d"),
        "description": merchant,
        "amount": amount
    })


# generate anomalies
for i in range(20):

    date = start_date + timedelta(days=random.randint(0, 60))

    merchant = random.choice(anomaly_merchants)

    amount = random.randint(50000, 150000)

    data.append({
        "date": date.strftime("%Y-%m-%d"),
        "description": merchant,
        "amount": amount
    })


df = pd.DataFrame(data)

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("data/transactions_large.csv", index=False)

print("Dataset generated: data/transactions_large.csv")