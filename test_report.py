import pandas as pd
from tools.categorizer import categorize_dataframe
from tools.anomaly_detector import detect_anomalies
from tools.report_generator import generate_report

df = pd.read_csv("data/sample_transactions.csv")

df = categorize_dataframe(df)

anomalies = detect_anomalies(df)

report = generate_report(df, anomalies)

print(report)