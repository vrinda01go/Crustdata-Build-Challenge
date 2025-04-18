from flask import Flask, request, jsonify
import pyautogui
import time
import subprocess
import pygetwindow as gw
import pyperclip

from automation_task import login_linkedin, search_jobs, check_proxy_ip

app = Flask(__name__)

@app.route("/interact", methods=["POST"])
def interact():
    data = request.get_json()
    command = data.get("command", "").lower()

    if "search for" in command and "on wikipedia" in command:
        query = command.split("search for")[-1].split("on wikipedia")[0].strip()

        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([
            chrome_path,
            "--user-data-dir=C:\\Users\\workstation\\ai_browser\\chrome_proxy",
            "--new-tab",
            "https://www.wikipedia.org"
        ], shell=True)

        time.sleep(5)

        try:
            chrome_window = next(w for w in gw.getWindowsWithTitle("Wikipedia") if not w.isMinimized)
            chrome_window.activate()
            time.sleep(1)
        except Exception as e:
            return jsonify({"error": f"Failed to activate Chrome window: {str(e)}"})

        pyautogui.moveTo(727, 966, duration=0.5)  # Update this if needed
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.write(query, interval=0.05)
        pyautogui.press("enter")

        return jsonify({"result": f"Searched '{query}' on Wikipedia tab."})

    return jsonify({"error": "Command not recognized."})


@app.route("/login_and_search", methods=["POST"])
def login_and_search():
    data = request.get_json()
    login_linkedin(data["username"], data["password"])
    search_jobs(data["search"])
    return jsonify({"result": "Completed login and search."})


# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         # Step 1: Focus Chrome window
#         win = next(w for w in gw.getWindowsWithTitle("Wikipedia") if not w.isMinimized)
#         win.activate()
#         time.sleep(1.5)

#         # Step 2: Open DevTools
#         pyautogui.hotkey("ctrl", "shift", "j")
#         time.sleep(2)

#         # Step 3: Focus console input manually
#         pyautogui.click(x=978, y=588)  # ⬅️ Update this with your own console input coordinates
#         time.sleep(1)

#         # Step 4: Inject simple clipboard test first
#         js_script = """
# (() => {
#   const result = Array.from(document.querySelectorAll('p'))
#     .map(el => el.innerText)
#     .filter(Boolean)
#     .slice(0, 5);

#   console.log("RESULTS:", result);
# })();

# """

#         pyperclip.copy(js_script)
#         pyautogui.hotkey("ctrl", "v")
#         pyautogui.press("enter")

#         time.sleep(2.5)  # wait for clipboard update

#         # Step 5: Close DevTools
#         pyautogui.hotkey("ctrl", "shift", "j")
#         time.sleep(0.5)

#         # Step 6: Read from clipboard
#         extracted = pyperclip.paste()

#         if not extracted.strip():
#             return jsonify({
#                 "result": "Extracted via JS",
#                 "text": "[Clipboard was empty — script may not have executed]"
#             })

#         return jsonify({
#             "result": "Extracted via JS",
#             "text": extracted[:2000]
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)})

@app.route("/extract", methods=["POST"])
def extract():
    try:
        win = next(w for w in gw.getWindowsWithTitle("Wikipedia") if not w.isMinimized)
        win.activate()
        time.sleep(1.5)

        # Open DevTools
        pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(2)

        # Focus input prompt
        pyautogui.click(x=978, y=588)  # Replace with your console input position
        time.sleep(0.5)

        # Write JS into clipboard and paste
        js_script = """
(() => {
  const result = Array.from(document.querySelectorAll('p'))
    .map(el => el.innerText)
    .filter(Boolean)
    .slice(0, 5)
    .join('\\n\\n');
  console.log(result);  // <-- log instead of copy
})();
"""
        pyperclip.copy(js_script)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        time.sleep(2)

        # Select console output and copy manually
        pyautogui.click(x=600, y=300)  # Click near console text
        # Click near the first log result line (tweak coords based on your screen)
        pyautogui.moveTo(x=880, y=320)
        pyautogui.click()
        time.sleep(0.3)

        # Triple-click to select the entire line (can simulate with double-click + drag if needed)
        pyautogui.click(clicks=2, interval=0.2)
        time.sleep(0.3)

        # Copy just that line
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)

        pyautogui.hotkey("ctrl", "shift", "j")  # Close DevTools

        # Read final clipboard
        extracted = pyperclip.paste()

        if not extracted.strip():
            return jsonify({
                "result": "Console executed but clipboard empty",
                "text": "[Check if Chrome DevTools is allowing selection]"
            })

        return jsonify({
            "result": "Extracted via console + copy",
            "text": extracted[:2000]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/proxy_test", methods=["GET"])
def proxy_test():
    check_proxy_ip()
    return jsonify({"result": "Opened https://httpbin.org/ip to verify proxy."})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
    