def generate_report(df, anomalies):

    total_spend = df["amount"].sum()

    report = "MONTHLY EXPENSE SUMMARY\n"
    report += "----------------------------\n"

    report += f"Total Spend: ₹{total_spend}\n"
    report += f"Total Transactions: {len(df)}\n"
    report += f"Anomalies Detected: {len(anomalies)}\n\n"

    report += "Anomaly Details:\n"

    if len(anomalies) == 0:
        report += "No anomalies detected.\n"
    else:
        for anomaly in anomalies:

            description = anomaly.get("description", "Unknown")
            amount = anomaly.get("amount", "Unknown")

            report += f"- {description} ₹{amount} (Unusual transaction)\n"

    return report