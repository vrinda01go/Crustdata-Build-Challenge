from flask import Flask, request, jsonify, session
import json
import time
from chrome_controller import ChromeController

app = Flask(__name__)
app.secret_key = 'some-secret-key'  # Needed for session

@app.route("/interact", methods=["POST"])
def interact():
    data = request.get_json()
    command = data.get("command", "").lower()
    print("Command received:", command)

    try:
        browser = ChromeController()

        if "wikipedia" in command and "search for" in command:
            topic = command.split("search for")[-1].split("on wikipedia")[0].strip()
            session["last_topic"] = topic

            search_url = f"https://en.wikipedia.org/w/index.php?search={topic.replace(' ', '+')}"
            browser.navigate_to(search_url)
            time.sleep(3)
            browser.evaluate_js("""
                (() => {
                    const firstLink = document.querySelector('.mw-search-result-heading a');
                    if (firstLink) firstLink.click();
                })();
            """)
            time.sleep(3)
            return jsonify({"result": f"Opened Wikipedia article for '{topic}'."})

        # elif "get reviews of" in command:
        #     series = command.split("get reviews of")[-1].strip()
        #     search_query = f"{series} series reviews"

        #     browser.navigate_to(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            
        #     # ⏳ Gracefully wait for results to load and click a result (if needed)
        #     browser.evaluate_js("""
        #         (() => {
        #             let tries = 0;
        #             const interval = setInterval(() => {
        #                 const el = document.querySelector('.tF2Cxc a');  // Google result links
        #                 if (el) {
        #                     el.click();  // Clicks the first result
        #                     clearInterval(interval);
        #                 }
        #                 if (++tries > 10) clearInterval(interval);
        #             }, 500);
        #         })()
        #     """)
            
        #     return jsonify({"result": f"Searched for reviews of '{series}' on Google and clicked the first result."})
        elif "get reviews of" in command:
            series = command.split("get reviews of")[-1].strip()
            search_query = f"{series} series reviews"

            browser.navigate_to(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            
            # Wait for and click the first search result
            browser.wait_and_click(".tF2Cxc a")

            return jsonify({"result": f"Searched for reviews of '{series}' on Google and clicked the first result."})
        
        elif "where can i see it" in command:
            topic = session.get("last_topic")
            if not topic:
                return jsonify({"error": "No topic stored from previous interaction."})

            # Form query like "Where can I watch Big Bang Theory"
            search_query = f"where to watch {topic}"
            browser.navigate_to(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            return jsonify({"result": f"Searched where to watch '{topic}' on Google."})


        elif "get reviews" in command:
            topic = session.get("last_topic")
            if not topic:
                return jsonify({"error": "No topic stored from previous interaction."})

            search_query = f"{topic} series reviews"
            browser.navigate_to(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            time.sleep(3)

            result = browser.evaluate_js("""
                (() => {
                    const snippets = Array.from(document.querySelectorAll('div[data-content-feature="1"]'))
                        .map(e => e.innerText)
                        .filter(Boolean)
                        .slice(0, 5);
                    return JSON.stringify(snippets);
                })()
            """)
            parsed = json.loads(result)

            print(f"\n🔍 Reviews for {topic}:\n")
            for idx, snippet in enumerate(parsed, 1):
                print(f"{idx}. {snippet}\n")

            return jsonify({"result": f"Fetched reviews for '{topic}' and printed to console."})

        return jsonify({"result": "Command not recognized."})

        return jsonify({"result": "Command not recognized."})
    

    except Exception as e:
        return jsonify({"error": str(e)})

# @app.route("/login_and_search", methods=["POST"])
# def login_and_search():
#     try:
#         data = request.get_json()
#         browser = ChromeController()

#         # Step 1: Go to login
#         browser.navigate_to("https://www.linkedin.com/login")

#         # Detect presence of CAPTCHA
#         is_captcha = browser.evaluate_js("""
#             (() => {
#                 return !!document.querySelector('iframe[src*="captcha"]') ||
#                     !!document.querySelector('[id*="captcha"], .captcha');
#             })()
#         """)

#         if "true" in is_captcha:
#             return jsonify({"error": "CAPTCHA detected. Manual intervention needed."})


#         # Step 2: Fill login details
#         browser.evaluate_js(f'''
#             document.querySelector("#username").value = "{data["username"]}";
#             document.querySelector("#password").value = "{data["password"]}";
#             document.querySelector("button[type=submit]").click();
#         ''')

#         time.sleep(5)  # wait for login

#         # Step 3: Go to job search
#         search_query = data["search"]
#         browser.navigate_to(f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}")

#         return jsonify({"result": f"Searched LinkedIn jobs for '{search_query}'."})
#     except Exception as e:
#         return jsonify({"error": str(e)})

## func for captcha detection
# @app.route("/login_and_search", methods=["POST"])
# def login_and_search():
#     try:
#         data = request.get_json()
#         browser = ChromeController()

#         # Navigate to Reddit login page
#         browser.navigate_to("https://www.reddit.com/login/")
#         time.sleep(5)  # Allow page to load

#         # Fill in login credentials and attempt login
#         browser.evaluate_js(f'''
#             (() => {{
#                 const username = document.querySelector("input#loginUsername");
#                 const password = document.querySelector("input#loginPassword");
#                 const button = document.querySelector("button[type='submit']");

#                 if (username && password && button) {{
#                     username.value = "{data["username"]}";
#                     password.value = "{data["password"]}";
#                     button.click();
#                 }}
#             }})()
#         ''')
#         time.sleep(6)  # wait for potential redirect or CAPTCHA

#         # CAPTCHA detection logic (Cloudflare or Reddit-specific)
#         is_captcha = browser.evaluate_js("""
#             (() => {
#                 return !!document.querySelector('iframe[src*="captcha"]') ||
#                        !!document.querySelector('[id*="captcha"], .captcha') ||
#                        !!document.querySelector('[class*="captcha"]') ||
#                        !!document.querySelector('div[class*="Challenge"]') || 
#                        !!document.querySelector('div[aria-label*="security check"]');
#             })()
#         """)

#         if "true" in is_captcha:
#             return jsonify({"error": "CAPTCHA detected on Reddit login. Manual resolution required."})

#         return jsonify({"result": "Reddit login attempted. No CAPTCHA detected."})

#     except Exception as e:
#         return jsonify({"error": str(e)})


## func to check if it is login already ##
# @app.route("/login_and_search", methods=["POST"])
# def login_and_search():
#     try:
#         data = request.get_json()
#         browser = ChromeController()

#         browser.navigate_to("https://www.linkedin.com/login/")
#         time.sleep(5)

#         # ✅ Check if already logged in
#         already_logged_in = browser.evaluate_js("""
#             (() => {
#                 return !!document.querySelector('header img[alt*="User Avatar"]') ||
#                        !!document.querySelector('[data-testid="user-icon"]') ||
#                        !!document.querySelector('a[href*="/user/"]');
#             })()
#         """)

#         if "true" in already_logged_in:
#             return jsonify({"result": "Already logged in. Skipping login step."})

#         # 🧪 Proceed to login
#         browser.evaluate_js(f'''
#             (() => {{
#                 const username = document.querySelector("input#loginUsername");
#                 const password = document.querySelector("input#loginPassword");
#                 const button = document.querySelector("button[type='submit']");

#                 if (username && password && button) {{
#                     username.value = "{data["username"]}";
#                     password.value = "{data["password"]}";
#                     button.click();
#                 }}
#             }})()
#         ''')

#         time.sleep(6)

#         # 🔒 CAPTCHA check
#         is_captcha = browser.evaluate_js("""
#             (() => {
#                 return !!document.querySelector('iframe[src*="captcha"]') ||
#                        !!document.querySelector('[id*="captcha"], .captcha') ||
#                        !!document.querySelector('[class*="captcha"]') ||
#                        !!document.querySelector('div[class*="Challenge"]') || 
#                        !!document.querySelector('div[aria-label*="security check"]');
#             })()
#         """)

#         if "true" in is_captcha:
#             return jsonify({"error": "CAPTCHA detected on Reddit login. Manual resolution required."})

#         return jsonify({"result": "Linkedin login attempted. No CAPTCHA detected."})

#     except Exception as e:
#         return jsonify({"error": str(e)})
@app.route("/login_and_search", methods=["POST"])
def login_and_search():
    try:
        data = request.get_json()
        browser = ChromeController()

        browser.navigate_to("https://www.linkedin.com/login")

        browser.evaluate_js(f'''
            document.querySelector("#username").value = "{data["username"]}";
            document.querySelector("#password").value = "{data["password"]}";
            document.querySelector("button[type=submit]").click();
        ''')

        time.sleep(5)

        # Graceful recovery logic
        browser.navigate_to("https://www.linkedin.com/feed/")  # Expected dashboard URL
        time.sleep(3)

        page_loaded = browser.evaluate_js("""
            (() => {
                return !!document.querySelector('div.feed-identity-module, .scaffold-finite-scroll') || false;
            })()
        """)

        if "false" in page_loaded:
            raise Exception("LinkedIn dashboard didn't load. Possibly logged out or invalid session.")

        return jsonify({"result": "Logged in and reached LinkedIn dashboard."})

    except Exception as e:
        browser.navigate_to("https://www.linkedin.com/login")
        return jsonify({"error": f"Recovered to login page due to: {str(e)}"})

@app.route("/get_rating", methods=["POST"])
def get_rating():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Missing query"}), 400

        browser = ChromeController()
        browser.navigate_to(f"https://www.google.com/search?q={query.replace(' ', '+')}+rating")
        time.sleep(3)

        # Try to extract the rating
        result = browser.evaluate_js("""
            (() => {
                const ratingElement = document.querySelector('div span.gsrt');
                if (ratingElement) return ratingElement.innerText;

                const altRating = document.querySelector('div[aria-label*="stars"], div span[aria-label*="stars"]');
                if (altRating) return altRating.innerText;

                const starBased = Array.from(document.querySelectorAll('span'))
                  .filter(span => span.innerText.match(/^\\d(\\.\\d)?\\/\\d$/));
                if (starBased.length > 0) return starBased[0].innerText;

                return null;
            })()
        """)

        if not result or "null" in result:
            return jsonify({"error": "No rating found"})

        return jsonify({"result": f"Rating: {json.loads(result)}"})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/extract", methods=["POST"])
def extract():
    try:
        browser = ChromeController()

        # Optional: show current page title for debug
        page_title = browser.evaluate_js("document.title")
        print(f"🧭 Current page: {page_title}")

        js_result = browser.evaluate_js("""
            (() => {
                try {
                    const title = document.querySelector('#firstHeading')?.innerText || "";

                    const contentDiv = document.querySelector('#mw-content-text');
                    if (!contentDiv) return JSON.stringify({ error: "Content not found" });

                    const elements = Array.from(contentDiv.querySelectorAll('p, ul, ol'))
                        .map(el => el.innerText.trim())
                        .filter(text => text.length > 0);

                    const full_text = elements.join('\\n\\n');

                    const infobox = {};
                    const rows = document.querySelectorAll('.infobox tr');
                    rows.forEach(row => {
                        const key = row.querySelector('th')?.innerText;
                        const value = row.querySelector('td')?.innerText;
                        if (key && value) infobox[key.trim()] = value.trim();
                    });

                    return JSON.stringify({ title, content: full_text, infobox });
                } catch (err) {
                    return JSON.stringify({ error: "JS Exception: " + err.message });
                }
            })()
        """)

        try:
            parsed = json.loads(js_result)
        except Exception as parse_err:
            print("⚠️ Failed to parse JS result:", js_result)
            return jsonify({"error": f"JSON parse error: {str(parse_err)}"})

        if "error" in parsed:
            print("⚠️ JS-side error:", parsed["error"])
            return jsonify({"error": parsed["error"]})

        print(f"\n📘 Title: {parsed.get('title', 'Unknown')}\n")
        print(parsed.get("content", "")[:2500])  # preview first 1500 chars

        return jsonify({"result": parsed})

    except Exception as e:
        print("🔥 Python-side error:", str(e))
        return jsonify({"error": str(e)})


@app.route("/proxy_test", methods=["GET"])
def proxy_test():
    try:
        browser = ChromeController()
        browser.navigate_to("https://httpbin.org/ip")
        time.sleep(3)
        ip = browser.evaluate_js("document.body.innerText")
        print("🧪 Proxy Output:\n", ip)
        return jsonify({"result": json.loads(ip)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(port=8000, debug=True)

##-----till here ------------------

