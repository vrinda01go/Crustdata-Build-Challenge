import schedule
import time
import requests

def task():
    print("⏰ Running scheduled task...")
    response = requests.post("http://localhost:8000/login_and_search", json={
        "username": "YOUR_EMAIL",
        "password": "YOUR_PASSWORD",
        "search": "python developer"
    })
    print(response.json())

# Run every 30 minutes
schedule.every(5).seconds.do(task)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
