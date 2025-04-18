import time
import requests
from datetime import datetime

def run_command(command):
    try:
        response = requests.post(
            "http://localhost:8000/interact",
            json={"command": command},
            headers={"Content-Type": "application/json"}
        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Executed: {command}")
        print(response.json())
    except Exception as e:
        print(f"Failed to execute '{command}': {e}")

# 🧠 Define periodic tasks
TASKS = [
    "open linkedin and search for frontend developer",
    "search reddit for python debugging tips"
]

INTERVAL_MINUTES = 0.1  # set your desired interval here

if __name__ == "__main__":
    while True:
        for task in TASKS:
            run_command(task)
        print(f"Sleeping for {INTERVAL_MINUTES} minutes...")
        time.sleep(INTERVAL_MINUTES * 60)
