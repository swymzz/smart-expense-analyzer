import sqlite3
import pandas as pd


DB_NAME = "analysis.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        transactions INTEGER,
        anomalies INTEGER,
        runtime REAL
    )
    """)

    conn.commit()
    conn.close()


def save_analysis(transactions, anomalies, runtime):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis_history (transactions, anomalies, runtime)
    VALUES (?, ?, ?)
    """, (transactions, anomalies, runtime))

    conn.commit()
    conn.close()


def load_history():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql(
        "SELECT * FROM analysis_history ORDER BY run_time DESC",
        conn
    )

    conn.close()

    return df