import pandas as pd
from tools.categorizer import categorize_dataframe

df = pd.read_csv("data/sample_transactions.csv")

df = categorize_dataframe(df)

print(df)