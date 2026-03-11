import pandas as pd
from tools.categorizer import categorize_dataframe
from tools.anomaly_detector import detect_anomalies

df = pd.read_csv("data/sample_transactions.csv")

df = categorize_dataframe(df)

anomalies = detect_anomalies(df)

print(anomalies)