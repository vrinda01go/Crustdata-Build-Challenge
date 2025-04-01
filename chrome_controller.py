import json
import requests
from websocket import create_connection

class ChromeController:
    def __init__(self, ws_url=None):
        if ws_url is None:
            # Fetch WebSocket debugger URL from local Chrome instance
            response = requests.get("http://localhost:9222/json")
            targets = response.json()
            ws_url = targets[0]["webSocketDebuggerUrl"]  # Get first target

        self.ws = create_connection(ws_url)

    def navigate_to(self, url):
        self.ws.send(json.dumps({
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": url}
        }))
        return self.ws.recv()

    def evaluate_js(self, expression):
        self.ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": expression}
        }))
        return self.ws.recv()

    def close(self):
        self.ws.close()
