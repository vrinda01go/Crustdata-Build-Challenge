# from flask import Flask, request, jsonify
# import threading
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import requests

# app = Flask(__name__)

# memory = {
#     "last_command": None,
#     "last_query": None,
#     "context": {}
# }

# # === NATURAL LANGUAGE INTERACT WITH CONTEXT ===
# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     memory["last_command"] = command

#     if "search reddit for" in command:
#         query = command.split("search reddit for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url

#     elif "search for" in command and "reddit" not in command:
#         # Extend previous query
#         extension = command.split("search for")[-1].strip()
#         if memory.get("last_query"):
#             query = f"{memory['last_query']} {extension}"
#             memory["last_query"] = query
#             url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#             memory["context"]["last_url"] = url
#         else:
#             return jsonify({"error": "No previous context to extend."})

#     elif "open last reddit link" in command:
#         url = memory.get("context", {}).get("last_url")
#         if not url:
#             return jsonify({"error": "No previous Reddit link stored in memory."})
#     else:
#         return jsonify({"error": "Command not understood."})

#     try:
#         chrome_window = next(w for w in gw.getAllWindows() if "chrome" in w.title.lower() and not w.isMinimized)
#         chrome_window.activate()
#         time.sleep(1)

#         pyautogui.hotkey("ctrl", "t")
#         time.sleep(0.5)
#         pyautogui.write(url, interval=0.03)
#         pyautogui.press("enter")
#         return jsonify({"result": f"Opened Reddit search for: {url}"})

#     except Exception as e:
#         return jsonify({"error": f"Failed to open Reddit: {str(e)}"})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
############# conversation memory code ends ############################



# from flask import Flask, request, jsonify
# import threading
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import requests
# from chrome_controller import ChromeController  # Add CDP control

# app = Flask(__name__)

# memory = {
#     "last_command": None,
#     "last_query": None,
#     "context": {}
# }

# # === NATURAL LANGUAGE INTERACT WITH CONTEXT ===
# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     memory["last_command"] = command
#     chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

#     use_incognito = False
#     login_attempt = False
#     url = None

#     if "search reddit for" in command:
#         query = command.split("search reddit for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "open reddit login page" in command:
#         url = "https://www.reddit.com/login"
#         use_incognito = True
#         login_attempt = True

#     elif "open linkedin and search for" in command:
#         query = command.split("open linkedin and search for")[-1].strip()
#         url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"

#     elif "search for" in command and "reddit" not in command:
#         extension = command.split("search for")[-1].strip()
#         if memory.get("last_query"):
#             query = f"{memory['last_query']} {extension}"
#             memory["last_query"] = query
#             url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#             memory["context"]["last_url"] = url
#             use_incognito = True
#         else:
#             return jsonify({"error": "No previous context to extend."})

#     elif "open last reddit link" in command:
#         url = memory.get("context", {}).get("last_url")
#         if not url:
#             return jsonify({"error": "No previous Reddit link stored in memory."})
#         use_incognito = True

#     else:
#         return jsonify({"error": "Command not understood."})

#     try:
#         if use_incognito:
#             subprocess.Popen([
#                 chrome_path,
#                 "--incognito",
#                 url
#             ], shell=True)

#             if login_attempt:
#                 time.sleep(8)
#                 try:
#                     login_win = next(w for w in gw.getWindowsWithTitle("Reddit") if not w.isMinimized)
#                     login_win.activate()
#                     time.sleep(1)
#                     pyautogui.click(x=10, y=10)
#                     time.sleep(1)

#                     pyautogui.alert("Chrome should now be focused. Clicking username box next.")

#                     pyautogui.moveTo(741, 697, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakeuser123", interval=0.1)

#                     pyautogui.moveTo(697, 806, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakepassword456", interval=0.1)

#                     pyautogui.moveTo(745, 920, duration=0.5)
#                     pyautogui.click()
#                     time.sleep(5)

#                     # Use ChromeController to check for CAPTCHA in DOM
#                     browser = ChromeController()
#                     captcha_result = browser.evaluate_js("""
#                         (() => {
#                             return !!document.querySelector('iframe[src*="captcha"]') ||
#                                    !!document.querySelector('[id*="captcha"], .captcha') ||
#                                    !!document.querySelector('[class*="captcha"]') ||
#                                    !!document.querySelector('div[class*="Challenge"]') || 
#                                    !!document.querySelector('div[aria-label*="security check"]');
#                         })()
#                     """)

#                     if "true" in captcha_result:
#                         return jsonify({"result": f"Tried login to {url}", "warning": "⚠️ CAPTCHA detected via DOM."})

#                 except Exception as e:
#                     return jsonify({"error": f"Login automation failed: {str(e)}"})

#                 return jsonify({"result": f"Tried login to {url}", "note": "No CAPTCHA detected."})

#             return jsonify({"result": f"Opened Reddit in incognito: {url}"})

#         else:
#             chrome_window = next(w for w in gw.getAllWindows() if "chrome" in w.title.lower() and not w.isMinimized)
#             chrome_window.activate()
#             time.sleep(1)

#             pyautogui.hotkey("ctrl", "t")
#             time.sleep(0.5)
#             pyautogui.write(url, interval=0.03)
#             pyautogui.press("enter")
#             return jsonify({"result": f"Opened link: {url}"})

#     except Exception as e:
#         return jsonify({"error": f"Failed to open browser: {str(e)}"})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
########### CAPTCHA AND MEMORY CONVERSATION CODE ENDS ################

# from flask import Flask, request, jsonify, session
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import json
# from chrome_controller import ChromeController
# import requests

# app = Flask(__name__)
# app.secret_key = 'some-secret-key'  # Needed for session

# def wait_for_chrome_debugger(timeout=10):
#     for _ in range(timeout * 2):
#         try:
#             r = requests.get("http://localhost:9222/json")
#             if r.status_code == 200:
#                 return True
#         except:
#             pass
#         time.sleep(0.5)
#     raise Exception("Chrome DevTools not available on port 9222")

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     print("Command received:", command)

#     try:
#         if "open linkedin and search for" in command:
#             query = command.split("open linkedin and search for")[-1].strip()
#             session["last_topic"] = query

#             # Launch Chrome with required flags
#             subprocess.Popen(
#                 f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" '
#                 f'--remote-debugging-port=9222 '
#                 f'--remote-allow-origins=* '
#                 f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#                 f'--no-first-run --no-default-browser-check '
#                 f'"https://www.linkedin.com/jobs/search/?keywords={query.replace(" ", "%20")}"',
#                 shell=True
#             )
#             return jsonify({"result": f"Opened LinkedIn job search for: {query}"})

#         elif "check linkedin login" in command:
#             wait_for_chrome_debugger()
#             browser = ChromeController()
#             result = browser.evaluate_js("""
#                 (() => {
#                     try {
#                         return !!document.querySelector('img.global-nav__me-photo') ||
#                                !!document.querySelector('a[href*="/mynetwork/"]') ||
#                                !!document.body.innerText.includes("Welcome,");
#                     } catch (e) {
#                         return false;
#                     }
#                 })()
#             """)
#             raw = json.loads(result)
#             val = raw.get("result", {}).get("result", {}).get("value", False)

#             msg = "✅ You are already logged in to LinkedIn." if val else "❌ You are not logged in to LinkedIn."
#             return jsonify({
#                 "result": "Checked LinkedIn login",
#                 "logged_in": val,
#                 "message": msg
#             })

#         elif "login to linkedin" in command:
#             subprocess.Popen(
#                 f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" '
#                 f'--remote-debugging-port=9222 '
#                 f'--remote-allow-origins=* '
#                 f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#                 f'--no-first-run --no-default-browser-check "https://www.linkedin.com/login"',
#                 shell=True
#             )
#             time.sleep(8)
#             login_win = next(w for w in gw.getWindowsWithTitle("LinkedIn") if not w.isMinimized)
#             login_win.activate()
#             time.sleep(1)

#             pyautogui.moveTo(750, 450)
#             pyautogui.click()
#             pyautogui.write("your_username_here", interval=0.1)

#             pyautogui.moveTo(750, 520)
#             pyautogui.click()
#             pyautogui.write("your_password_here", interval=0.1)

#             pyautogui.moveTo(750, 600)
#             pyautogui.click()
#             return jsonify({"result": "Tried to log into LinkedIn with pyautogui."})

#         else:
#             return jsonify({"result": "Command not recognized."})

#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
### LOGIN MANAGEMENT ENDS #####


# from flask import Flask, request, jsonify
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import json
# import requests
# from chrome_controller import ChromeController

# app = Flask(__name__)

# memory = {
#     "last_command": None,
#     "last_query": None,
#     "context": {},
#     "logged_in": False
# }

# def wait_for_chrome_debugger(timeout=10):
#     for _ in range(timeout * 2):
#         try:
#             r = requests.get("http://localhost:9222/json")
#             if r.status_code == 200:
#                 return True
#         except:
#             pass
#         time.sleep(0.5)
#     raise Exception("Chrome DevTools not available on port 9222")

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     memory["last_command"] = command
#     chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

#     use_incognito = False
#     login_attempt = False
#     url = None

#     if "search reddit for" in command:
#         query = command.split("search reddit for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "open reddit login page" in command:
#         url = "https://www.reddit.com/login"
#         use_incognito = True
#         login_attempt = True

#     elif "open linkedin and search for" in command:
#         query = command.split("open linkedin and search for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url

#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check '
#             f'"{url}"',
#             shell=True
#         )

#         return jsonify({"result": f"Opened LinkedIn job search for: {query}"})

#     elif "check linkedin login" in command:
#         wait_for_chrome_debugger()
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 try {
#                     return !!document.querySelector('img.global-nav__me-photo') ||
#                            !!document.querySelector('a[href*="/mynetwork/"]') ||
#                            !!document.body.innerText.includes("Welcome,");
#                 } catch (e) {
#                     return false;
#                 }
#             })()
#         """)
#         raw = json.loads(result)
#         val = raw.get("result", {}).get("result", {}).get("value", False)

#         memory["logged_in"] = val
#         msg = "✅ You are already logged in to LinkedIn." if val else "❌ You are not logged in to LinkedIn."
#         return jsonify({
#             "result": "Checked LinkedIn login",
#             "logged_in": val,
#             "message": msg
#         })

#     elif "login to linkedin" in command:
#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check "https://www.linkedin.com/login"',
#             shell=True
#         )
#         time.sleep(8)
#         login_win = next(w for w in gw.getWindowsWithTitle("LinkedIn") if not w.isMinimized)
#         login_win.activate()
#         time.sleep(1)

#         pyautogui.moveTo(750, 450)
#         pyautogui.click()
#         pyautogui.write("your_username_here", interval=0.1)

#         pyautogui.moveTo(750, 520)
#         pyautogui.click()
#         pyautogui.write("your_password_here", interval=0.1)

#         pyautogui.moveTo(750, 600)
#         pyautogui.click()
#         time.sleep(5)

#         wait_for_chrome_debugger()
#         browser = ChromeController()

#         captcha_check = browser.evaluate_js("""
#             (() => {
#                 return !!document.querySelector('iframe[src*="captcha"]') ||
#                        !!document.querySelector('[id*="captcha"], .captcha') ||
#                        !!document.querySelector('[class*="captcha"]') ||
#                        !!document.querySelector('div[class*="Challenge"]') ||
#                        !!document.querySelector('div[aria-label*="security check"]');
#             })()
#         """)

#         if "true" in captcha_check:
#             return jsonify({"result": "Tried login to LinkedIn", "warning": "⚠️ CAPTCHA detected via DOM."})

#         return jsonify({"result": "Login flow completed via pyautogui."})

#     elif "search for" in command and "reddit" not in command:
#         extension = command.split("search for")[-1].strip()
#         if memory.get("last_query"):
#             query = f"{memory['last_query']} {extension}"
#             memory["last_query"] = query
#             url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#             memory["context"]["last_url"] = url
#             use_incognito = True
#         else:
#             return jsonify({"error": "No previous context to extend."})

#     elif "open last reddit link" in command:
#         url = memory.get("context", {}).get("last_url")
#         if not url:
#             return jsonify({"error": "No previous Reddit link stored in memory."})
#         use_incognito = True

#     else:
#         return jsonify({"error": "Command not understood."})

#     try:
#         if use_incognito:
#             subprocess.Popen([
#                 chrome_path,
#                 "--incognito",
#                 url
#             ], shell=True)

#             if login_attempt:
#                 time.sleep(8)
#                 try:
#                     login_win = next(w for w in gw.getWindowsWithTitle("Reddit") if not w.isMinimized)
#                     login_win.activate()
#                     time.sleep(1)
#                     pyautogui.click(x=10, y=10)
#                     time.sleep(1)

#                     pyautogui.alert("Chrome should now be focused. Clicking username box next.")

#                     pyautogui.moveTo(741, 697, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakeuser123", interval=0.1)

#                     pyautogui.moveTo(697, 806, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakepassword456", interval=0.1)

#                     pyautogui.moveTo(745, 920, duration=0.5)
#                     pyautogui.click()
#                     time.sleep(5)

#                     browser = ChromeController()
#                     captcha_result = browser.evaluate_js("""
#                         (() => {
#                             return !!document.querySelector('iframe[src*="captcha"]') ||
#                                    !!document.querySelector('[id*="captcha"], .captcha') ||
#                                    !!document.querySelector('[class*="captcha"]') ||
#                                    !!document.querySelector('div[class*="Challenge"]') || 
#                                    !!document.querySelector('div[aria-label*="security check"]');
#                         })()
#                     """)

#                     if "true" in captcha_result:
#                         return jsonify({"result": f"Tried login to {url}", "warning": "⚠️ CAPTCHA detected via DOM."})

#                 except Exception as e:
#                     return jsonify({"error": f"Login automation failed: {str(e)}"})

#                 return jsonify({"result": f"Tried login to {url}", "note": "No CAPTCHA detected."})

#             return jsonify({"result": f"Opened Reddit in incognito: {url}"})

#         else:
#             chrome_window = next(w for w in gw.getAllWindows() if "chrome" in w.title.lower() and not w.isMinimized)
#             chrome_window.activate()
#             time.sleep(1)

#             pyautogui.hotkey("ctrl", "t")
#             time.sleep(0.5)
#             pyautogui.write(url, interval=0.03)
#             pyautogui.press("enter")
#             return jsonify({"result": f"Opened link: {url}"})

#     except Exception as e:
#         return jsonify({"error": f"Failed to open browser: {str(e)}"})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)

############## CODE RUNS TILL HERE #######################

# from flask import Flask, request, jsonify
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import json
# import requests
# from chrome_controller import ChromeController

# app = Flask(__name__)

# memory = {
#     "last_command": None,
#     "last_query": None,
#     "context": {},
#     "logged_in": False
# }

# def wait_for_chrome_debugger(timeout=10):
#     for _ in range(timeout * 2):
#         try:
#             r = requests.get("http://localhost:9222/json")
#             if r.status_code == 200:
#                 return True
#         except:
#             pass
#         time.sleep(0.5)
#     raise Exception("Chrome DevTools not available on port 9222")

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     memory["last_command"] = command
#     chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

#     use_incognito = False
#     login_attempt = False
#     url = None

#     if "search reddit for" in command:
#         query = command.split("search reddit for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "open reddit login page" in command:
#         url = "https://www.reddit.com/login"
#         use_incognito = True
#         login_attempt = True

#     elif "open linkedin and search for" in command:
#         query = command.split("open linkedin and search for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url

#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check '
#             f'"{url}"',
#             shell=True
#         )

#         return jsonify({"result": f"Opened LinkedIn job search for: {query}"})

#     elif "check linkedin login" in command:
#         wait_for_chrome_debugger()
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 try {
#                     return !!document.querySelector('img.global-nav__me-photo') ||
#                            !!document.querySelector('a[href*="/mynetwork/"]') ||
#                            !!document.body.innerText.includes("Welcome,");
#                 } catch (e) {
#                     return false;
#                 }
#             })()
#         """)
#         raw = json.loads(result)
#         val = raw.get("result", {}).get("result", {}).get("value", False)

#         memory["logged_in"] = val
#         msg = "✅ You are already logged in to LinkedIn." if val else "❌ You are not logged in to LinkedIn."
#         return jsonify({
#             "result": "Checked LinkedIn login",
#             "logged_in": val,
#             "message": msg
#         })

#     elif "open linkedin link" in command:
#         link = command.split("open linkedin link")[-1].strip()
#         url = link if link.startswith("http") else f"https://www.linkedin.com/{link}"
#         memory["context"]["last_url"] = url

#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check '
#             f'"{url}"',
#             shell=True
#         )

#         time.sleep(5)
#         wait_for_chrome_debugger()
#         browser = ChromeController()

#         invalid_page = browser.evaluate_js("""
#             (() => {
#                 return document.title.includes("Page Not Found") ||
#                        document.body.innerText.includes("This page doesn’t exist");
#             })()
#         """)

#         if "true" in invalid_page:
#             browser.navigate_to("https://www.linkedin.com/feed/")
#             return jsonify({"result": "Invalid LinkedIn page detected. Redirected to homepage."})

#         return jsonify({"result": f"Opened LinkedIn link: {url}"})

#     elif "open subreddit" in command:
#         sub = command.split("open subreddit")[-1].strip()
#         url = f"https://www.reddit.com/r/{sub}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "search for" in command and "reddit" not in command:
#         extension = command.split("search for")[-1].strip()
#         if memory.get("last_query"):
#             query = f"{memory['last_query']} {extension}"
#             memory["last_query"] = query
#             url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#             memory["context"]["last_url"] = url
#             use_incognito = True
#         else:
#             return jsonify({"error": "No previous context to extend."})

#     elif "open last reddit link" in command:
#         url = memory.get("context", {}).get("last_url")
#         if not url:
#             return jsonify({"error": "No previous Reddit link stored in memory."})
#         use_incognito = True

#     else:
#         return jsonify({"error": "Command not understood."})

#     try:
#         if use_incognito:
#             subprocess.Popen([
#                 chrome_path,
#                 "--incognito",
#                 url
#             ], shell=True)
#             return jsonify({"result": f"Opened Reddit in incognito: {url}"})

#     except Exception as e:
#         return jsonify({"error": f"Failed to open browser: {str(e)}"})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)

######### FULLY WORKING CODE EXCLUDING COMPATIBILITY ON VARIOUS OS #############

# from flask import Flask, request, jsonify
# import time
# import pyautogui
# import subprocess
# import pygetwindow as gw
# import json
# import requests
# from chrome_controller import ChromeController

# app = Flask(__name__)

# memory = {
#     "last_command": None,
#     "last_query": None,
#     "context": {},
#     "logged_in": False
# }

# def wait_for_chrome_debugger(timeout=10):
#     for _ in range(timeout * 2):
#         try:
#             r = requests.get("http://localhost:9222/json")
#             if r.status_code == 200:
#                 return True
#         except:
#             pass
#         time.sleep(0.5)
#     raise Exception("Chrome DevTools not available on port 9222")

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     memory["last_command"] = command
#     chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

#     use_incognito = False
#     login_attempt = False
#     url = None

#     if "search reddit for" in command:
#         query = command.split("search reddit for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "open reddit login page" in command:
#         url = "https://www.reddit.com/login"
#         use_incognito = True
#         login_attempt = True

#     elif "open linkedin and search for" in command:
#         query = command.split("open linkedin and search for")[-1].strip()
#         memory["last_query"] = query
#         url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
#         memory["context"]["last_url"] = url

#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check '
#             f'"{url}"',
#             shell=True
#         )

#         return jsonify({"result": f"Opened LinkedIn job search for: {query}"})

#     elif "check linkedin login" in command:
#         wait_for_chrome_debugger()
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 try {
#                     return !!document.querySelector('img.global-nav__me-photo') ||
#                            !!document.querySelector('a[href*="/mynetwork/"]') ||
#                            !!document.body.innerText.includes("Welcome,");
#                 } catch (e) {
#                     return false;
#                 }
#             })()
#         """)
#         raw = json.loads(result)
#         val = raw.get("result", {}).get("result", {}).get("value", False)

#         memory["logged_in"] = val
#         msg = "✅ You are already logged in to LinkedIn." if val else "❌ You are not logged in to LinkedIn."
#         return jsonify({
#             "result": "Checked LinkedIn login",
#             "logged_in": val,
#             "message": msg
#         })

#     elif "open linkedin link" in command:
#         link = command.split("open linkedin link")[-1].strip()
#         url = link if link.startswith("http") else f"https://www.linkedin.com/{link}"
#         memory["context"]["last_url"] = url

#         subprocess.Popen(
#             f'"{chrome_path}" '
#             f'--remote-debugging-port=9222 '
#             f'--remote-allow-origins=* '
#             f'--user-data-dir="C:\\Users\\workstation\\ai_browser\\linkedin_profile" '
#             f'--no-first-run --no-default-browser-check '
#             f'"{url}"',
#             shell=True
#         )

#         time.sleep(5)
#         wait_for_chrome_debugger()
#         browser = ChromeController()

#         invalid_page = browser.evaluate_js("""
#             (() => {
#                 return document.title.includes("Page Not Found") ||
#                        document.body.innerText.includes("This page doesn’t exist");
#             })()
#         """)

#         if "true" in invalid_page:
#             browser.navigate_to("https://www.linkedin.com/feed/")
#             return jsonify({"result": "Invalid LinkedIn page detected. Redirected to homepage."})

#         return jsonify({"result": f"Opened LinkedIn link: {url}"})

#     elif "open subreddit" in command:
#         sub = command.split("open subreddit")[-1].strip()
#         url = f"https://www.reddit.com/r/{sub}"
#         memory["context"]["last_url"] = url
#         use_incognito = True

#     elif "search for" in command and "reddit" not in command:
#         extension = command.split("search for")[-1].strip()
#         if memory.get("last_query"):
#             query = f"{memory['last_query']} {extension}"
#             memory["last_query"] = query
#             url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
#             memory["context"]["last_url"] = url
#             use_incognito = True
#         else:
#             return jsonify({"error": "No previous context to extend."})

#     elif "open last reddit link" in command:
#         url = memory.get("context", {}).get("last_url")
#         if not url:
#             return jsonify({"error": "No previous Reddit link stored in memory."})
#         use_incognito = True

#     else:
#         return jsonify({"error": "Command not understood."})

#     try:
#         if use_incognito:
#             subprocess.Popen([
#                 chrome_path,
#                 "--incognito",
#                 url
#             ], shell=True)

#             if login_attempt:
#                 time.sleep(8)
#                 try:
#                     login_win = next(w for w in gw.getWindowsWithTitle("Reddit") if not w.isMinimized)
#                     login_win.activate()
#                     time.sleep(1)
#                     pyautogui.click(x=10, y=10)
#                     time.sleep(1)

#                     pyautogui.alert("Chrome should now be focused. Clicking username box next.")

#                     pyautogui.moveTo(741, 697, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakeuser123", interval=0.1)

#                     pyautogui.moveTo(697, 806, duration=0.5)
#                     pyautogui.click()
#                     pyautogui.write("fakepassword456", interval=0.1)

#                     pyautogui.moveTo(745, 920, duration=0.5)
#                     pyautogui.click()
#                     time.sleep(5)

#                     browser = ChromeController()
#                     is_logged_in = browser.evaluate_js("""
#                         (() => {
#                             return !!document.querySelector('a[href*="/user/"]') ||
#                                    !!document.querySelector('header img[alt*="User"]');
#                         })()
#                     """)
#                     if "true" in is_logged_in:
#                         memory["logged_in"] = True

#                     captcha_result = browser.evaluate_js("""
#                         (() => {
#                             return !!document.querySelector('iframe[src*="captcha"]') ||
#                                    !!document.querySelector('[id*="captcha"], .captcha') ||
#                                    !!document.querySelector('[class*="captcha"]') ||
#                                    !!document.querySelector('div[class*="Challenge"]') || 
#                                    !!document.querySelector('div[aria-label*="security check"]');
#                         })()
#                     """)

#                     if "true" in captcha_result:
#                         return jsonify({"result": f"Tried login to {url}", "warning": "⚠️ CAPTCHA detected via DOM."})

#                     return jsonify({"result": f"Login attempt finished. Logged in: {memory['logged_in']}"})

#                 except Exception as e:
#                     return jsonify({"error": f"Login automation failed: {str(e)}"})

#             return jsonify({"result": f"Opened Reddit in incognito: {url}"})

#         else:
#             chrome_window = next(w for w in gw.getAllWindows() if "chrome" in w.title.lower() and not w.isMinimized)
#             chrome_window.activate()
#             time.sleep(1)

#             pyautogui.hotkey("ctrl", "t")
#             time.sleep(0.5)
#             pyautogui.write(url, interval=0.03)
#             pyautogui.press("enter")

#             time.sleep(5)
#             browser = ChromeController()
#             check_loaded = browser.evaluate_js("document.readyState")
#             if "complete" not in check_loaded:
#                 return jsonify({"result": "Page still loading. Waiting or retrying might help."})

#             valid = browser.evaluate_js("""
#                 (() => {
#                     const dialog = document.querySelector('div[role=dialog]');
#                     if (dialog && dialog.innerText.includes("Community not found")) return false;
#                     if (document.body.innerText.includes("something went wrong")) return false;
#                     return true;
#                 })()
#             """)
#             if "false" in valid:
#                 browser.navigate_to("https://www.reddit.com")
#                 return jsonify({"result": "Page was broken. Redirected to Reddit homepage."})

#             return jsonify({"result": f"Opened link: {url}"})

#     except Exception as e:
#         return jsonify({"error": f"Failed to open browser: {str(e)}"})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)



############### FULLY WORKING CODE ENDS ###################

from flask import Flask, request, jsonify
import time
import pyautogui
import subprocess
import pygetwindow as gw
import json
import requests
import platform
import os
from chrome_controller import ChromeController

app = Flask(__name__)

memory = {
    "last_command": None,
    "last_query": None,
    "context": {},
    "logged_in": False
}


def get_chrome_path():
    os_name = platform.system()
    if os_name == "Windows":
        return r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    elif os_name == "Darwin":  # macOS
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif os_name == "Linux":
        return "/usr/bin/google-chrome"
    else:
        raise Exception("Unsupported OS")


def wait_for_chrome_debugger(timeout=10):
    for _ in range(timeout * 2):
        try:
            r = requests.get("http://localhost:9222/json")
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    raise Exception("Chrome DevTools not available on port 9222")


@app.route("/interact", methods=["POST"])
def interact():
    data = request.get_json()
    command = data.get("command", "").lower()
    memory["last_command"] = command
    chrome_path = get_chrome_path()

    use_incognito = False
    login_attempt = False
    url = None

    if "search reddit for" in command:
        query = command.split("search reddit for")[-1].strip()
        memory["last_query"] = query
        url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
        memory["context"]["last_url"] = url
        use_incognito = True

    elif "open reddit login page" in command:
        url = "https://www.reddit.com/login"
        use_incognito = True
        login_attempt = True

    elif "open linkedin and search for" in command:
        query = command.split("open linkedin and search for")[-1].strip()
        memory["last_query"] = query
        url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
        memory["context"]["last_url"] = url

        subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9222",
            "--remote-allow-origins=*",
            f"--user-data-dir={os.path.expanduser('~')}/ai_browser/linkedin_profile",
            "--no-first-run",
            "--no-default-browser-check",
            url
        ])

        return jsonify({"result": f"Opened LinkedIn job search for: {query}"})

    elif "check linkedin login" in command:
        wait_for_chrome_debugger()
        browser = ChromeController()
        result = browser.evaluate_js("""
            (() => {
                try {
                    return !!document.querySelector('img.global-nav__me-photo') ||
                           !!document.querySelector('a[href*="/mynetwork/"]') ||
                           !!document.body.innerText.includes("Welcome,");
                } catch (e) {
                    return false;
                }
            })()
        """)
        raw = json.loads(result)
        val = raw.get("result", {}).get("result", {}).get("value", False)

        memory["logged_in"] = val
        msg = "✅ You are already logged in to LinkedIn." if val else "❌ You are not logged in to LinkedIn."
        return jsonify({
            "result": "Checked LinkedIn login",
            "logged_in": val,
            "message": msg
        })

    elif "open linkedin link" in command:
        link = command.split("open linkedin link")[-1].strip()
        url = link if link.startswith("http") else f"https://www.linkedin.com/{link}"
        memory["context"]["last_url"] = url

        subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9222",
            "--remote-allow-origins=*",
            f"--user-data-dir={os.path.expanduser('~')}/ai_browser/linkedin_profile",
            "--no-first-run",
            "--no-default-browser-check",
            url
        ])

        time.sleep(5)
        wait_for_chrome_debugger()
        browser = ChromeController()

        invalid_page = browser.evaluate_js("""
            (() => {
                const bodyText = document.body.innerText.toLowerCase();
                return bodyText.includes("page not found") ||
                       bodyText.includes("this page doesn’t exist") ||
                       document.title.toLowerCase().includes("linkedin") && document.title.toLowerCase().includes("error");
            })()
        """)

        if "true" in invalid_page:
            browser.navigate_to("https://www.linkedin.com/feed/")
            return jsonify({"result": "Invalid LinkedIn page detected. Redirected to homepage."})

        return jsonify({"result": f"Opened LinkedIn link: {url}"})

    elif "open subreddit" in command:
        sub = command.split("open subreddit")[-1].strip()
        url = f"https://www.reddit.com/r/{sub}"
        memory["context"]["last_url"] = url
        use_incognito = True

    elif "search for" in command and "reddit" not in command:
        extension = command.split("search for")[-1].strip()
        if memory.get("last_query"):
            query = f"{memory['last_query']} {extension}"
            memory["last_query"] = query
            url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}"
            memory["context"]["last_url"] = url
            use_incognito = True
        else:
            return jsonify({"error": "No previous context to extend."})

    elif "open last reddit link" in command:
        url = memory.get("context", {}).get("last_url")
        if not url:
            return jsonify({"error": "No previous Reddit link stored in memory."})
        use_incognito = True

    else:
        return jsonify({"error": "Command not understood."})

    try:
        if use_incognito:
            subprocess.Popen([
                chrome_path,
                "--incognito",
                url
            ])
            return jsonify({"result": f"Opened Reddit in incognito: {url}"})

        else:
            chrome_window = next(w for w in gw.getAllWindows() if "chrome" in w.title.lower() and not w.isMinimized)
            chrome_window.activate()
            time.sleep(1)

            pyautogui.hotkey("ctrl", "t")
            time.sleep(0.5)
            pyautogui.write(url, interval=0.03)
            pyautogui.press("enter")

            time.sleep(5)
            browser = ChromeController()
            check_loaded = browser.evaluate_js("document.readyState")
            if "complete" not in check_loaded:
                return jsonify({"result": "Page still loading. Waiting or retrying might help."})

            valid = browser.evaluate_js("""
                (() => {
                    const dialog = document.querySelector('div[role=dialog]');
                    if (dialog && dialog.innerText.includes("Community not found")) return false;
                    if (document.body.innerText.includes("something went wrong")) return false;
                    return true;
                })()
            """)
            if "false" in valid:
                browser.navigate_to("https://www.reddit.com")
                return jsonify({"result": "Page was broken. Redirected to Reddit homepage."})

            return jsonify({"result": f"Opened link: {url}"})

    except Exception as e:
        return jsonify({"error": f"Failed to open browser: {str(e)}"})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
