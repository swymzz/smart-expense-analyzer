import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

from database import init_db, save_analysis, load_history
from agent.state_machine import ExpenseAgent

# initialize database
init_db()

st.set_page_config(page_title="Smart Expense Analyzer", layout="wide")

st.title("💰 Smart Expense Analyzer")
st.write("Analyze financial transactions using an AI agent with anomaly detection.")

# ---------------------------------------------------
# RUN CONTROLS
# ---------------------------------------------------

st.subheader("⚙️ Run Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    start_agent = st.button("Start Agent")

with col2:
    reset_agent = st.button("Reset Agent")

with col3:
    seed_value = st.number_input("Seed", value=42)

with col4:
    scenario_choice = st.selectbox(
        "Choose Scenario",
        ["Upload CSV"] + os.listdir("scenarios")
    )

uploaded_file = None

if scenario_choice == "Upload CSV":
    uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])
else:
    uploaded_file = f"scenarios/{scenario_choice}"

if reset_agent:
    st.session_state.clear()
    st.rerun()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

if uploaded_file is not None:

    if isinstance(uploaded_file, str):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Transactions")
    st.dataframe(df, use_container_width=True)

    # ---------------------------------------------------
    # RUN AGENT
    # ---------------------------------------------------

    if start_agent:

        start_time = time.time()

        agent = ExpenseAgent(df)

        result = agent.run()

        end_time = time.time()
        runtime = round(end_time - start_time, 2)

        # extract results
        categorized_df = result["data"]
        anomalies = result["anomalies"]
        report = result["report"]
        logs = result["logs"]

        # save to database
        save_analysis(
            len(categorized_df),
            len(anomalies),
            runtime
        )

        st.success("Agent Run Completed")

        # ---------------------------------------------------
        # METRICS
        # ---------------------------------------------------

        st.subheader("📊 Dashboard Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transactions Processed", len(categorized_df))
        col2.metric("Anomalies Detected", len(anomalies))
        col3.metric("Runtime (seconds)", runtime)

        # ---------------------------------------------------
        # CATEGORY CHARTS
        # ---------------------------------------------------

        st.subheader("📊 Expense Breakdown by Category")

        category_spend = categorized_df.groupby("category")["amount"].sum().reset_index()

        col1, col2 = st.columns(2)

        with col1:
            bar_fig = px.bar(
                category_spend,
                x="category",
                y="amount",
                title="Spending by Category",
                color="category"
            )
            st.plotly_chart(bar_fig, use_container_width=True)

        with col2:
            pie_fig = px.pie(
                category_spend,
                values="amount",
                names="category",
                title="Category Distribution"
            )
            st.plotly_chart(pie_fig, use_container_width=True)

        # ---------------------------------------------------
        # TRANSACTIONS TABLE
        # ---------------------------------------------------

        st.subheader("Categorized Transactions")
        st.dataframe(categorized_df, use_container_width=True)

        # ---------------------------------------------------
        # ANOMALIES
        # ---------------------------------------------------

        st.subheader("🚨 Detected Anomalies")

        if len(anomalies) == 0:
            st.info("No anomalies detected")
        else:
            anomaly_df = pd.DataFrame(anomalies)

            st.dataframe(anomaly_df, use_container_width=True)

            st.subheader("📍 Anomaly Visualization")

            scatter_fig = px.scatter(
                anomaly_df,
                x="amount",
                y="category",
                color="amount",
                size="amount",
                title="Detected Anomalies"
            )

            st.plotly_chart(scatter_fig, use_container_width=True)

        # ---------------------------------------------------
        # REPORT
        # ---------------------------------------------------

        st.subheader("Monthly Expense Report")
        st.text(report)

        # ---------------------------------------------------
        # AGENT LOGS
        # ---------------------------------------------------

        st.subheader("🤖 Agent Activity Logs")

        logs_df = pd.DataFrame(logs)
        st.dataframe(logs_df, use_container_width=True)

# ---------------------------------------------------
# ANALYSIS HISTORY
# ---------------------------------------------------

st.subheader("📊 Analysis History")

history_df = load_history()

if len(history_df) == 0:
    st.info("No analysis history yet.")
else:
    st.dataframe(history_df, use_container_width=True)

    st.subheader("Anomalies per Run")
    st.bar_chart(history_df.set_index("run_time")["anomalies"])

# ---------------------------------------------------
# SCENARIO EVALUATION SYSTEM
# ---------------------------------------------------

st.subheader("🧪 Scenario Evaluation System")

if st.button("Run Scenario Evaluation"):

    scenario_folder = "scenarios"

    results = []

    for file in os.listdir(scenario_folder):

        if file.endswith(".csv"):

            path = os.path.join(scenario_folder, file)

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

    st.subheader("📊 Evaluation Results")

    st.dataframe(results_df, use_container_width=True)

    st.bar_chart(results_df.set_index("scenario")["anomalies_detected"])