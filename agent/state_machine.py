from enum import Enum
import uuid
import time

from tools.categorizer import categorize_transactions
from tools.anomaly_detector import detect_anomalies
from tools.report_generator import generate_report


class AgentState(Enum):
    IDLE = "IDLE"
    LOAD_DATA = "LOAD_DATA"
    CATEGORIZE = "CATEGORIZE"
    DETECT_ANOMALIES = "DETECT_ANOMALIES"
    GENERATE_REPORT = "GENERATE_REPORT"
    FINISHED = "FINISHED"


class StateMachine:

    def __init__(self):
        self.current_state = AgentState.IDLE
        self.history = []

    def transition(self, new_state):
        self.history.append({
            "from": self.current_state.value,
            "to": new_state.value
        })
        self.current_state = new_state

    def get_state(self):
        return self.current_state

    def get_history(self):
        return self.history


class ExpenseAgent:

    def __init__(self, df):

        self.run_id = str(uuid.uuid4())

        self.state = AgentState.IDLE

        self.df = df
        self.anomalies = None
        self.report = None

        self.logs = []

    def log(self, message):

        log_entry = {
            "run_id": self.run_id,
            "state": self.state.value,
            "message": message,
            "timestamp": time.time()
        }

        self.logs.append(log_entry)

    def load_data(self):

        self.state = AgentState.LOAD_DATA
        self.log("Transactions loaded from UI")

    def categorize(self):

        self.state = AgentState.CATEGORIZE
        self.log("Categorizing transactions")

        self.df = categorize_transactions(self.df)

    def detect_anomalies(self):

        self.state = AgentState.DETECT_ANOMALIES
        self.log("Detecting anomalies")

        self.df = detect_anomalies(self.df)

        self.anomalies = self.df[self.df["anomaly"] == 1].to_dict("records")

    def generate_report(self):

        self.state = AgentState.GENERATE_REPORT
        self.log("Generating report")

        self.report = generate_report(self.df, self.anomalies)

    def run(self):

        self.log("Agent started")

        self.load_data()
        self.categorize()
        self.detect_anomalies()
        self.generate_report()

        self.state = AgentState.FINISHED
        self.log("Run completed")

        return {
            "data": self.df,
            "anomalies": self.anomalies,
            "report": self.report,
            "logs": self.logs
        }