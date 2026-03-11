import json
import datetime
import os

class AgentLogger:

    def __init__(self, run_id):

        self.run_id = run_id

        os.makedirs("logs", exist_ok=True)

        self.file_path = f"logs/run_{run_id}.jsonl"

    def log(self, state, tool, message, data=None):

        log_entry = {
            "run_id": self.run_id,
            "state": state,
            "tool": tool,
            "message": message,
            "data": data,
            "timestamp": str(datetime.datetime.now())
        }

        with open(self.file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")