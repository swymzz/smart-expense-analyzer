import pandas as pd
import time
import os

from agent.state_machine import ExpenseAgent

SCENARIO_FOLDER = "scenarios"

results = []

for file in os.listdir(SCENARIO_FOLDER):

    if file.endswith(".csv"):

        path = os.path.join(SCENARIO_FOLDER, file)

        df = pd.read_csv(path)

        start = time.time()

        agent = ExpenseAgent(df)

        output = agent.run()

        runtime = round(time.time() - start, 2)

        anomalies = output["anomalies"]

        results.append({
            "scenario": file,
            "transactions": len(df),
            "anomalies_detected": len(anomalies),
            "runtime_seconds": runtime
        })

results_df = pd.DataFrame(results)

print("\nEvaluation Results\n")
print(results_df)

results_df.to_csv("evaluation_results.csv", index=False)

print("\nSaved evaluation_results.csv")