import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) == 0:
        return df

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(df[numeric_cols])

    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    return df