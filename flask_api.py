# from flask import Flask, request, jsonify
# from playwright.sync_api import sync_playwright
# import time

# app = Flask(__name__)

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     print("Received:", command)

#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch(headless=False)
#             page = browser.new_page()

#             if "wikipedia" in command and "search for" in command:
#                 # Extract search query
#                 query = command.split("search for")[-1].split("on wikipedia")[0].strip()

#                 # 1. Go to Wikipedia
#                 page.goto("https://www.wikipedia.org")

#                 # 2. Fill the search box
#                 page.fill("input[name='search']", query)
#                 page.keyboard.press("Enter")

#                 # 3. Wait and click first result if it's a disambiguation or search list
#                 page.wait_for_load_state("networkidle")
#                 time.sleep(2)

#                 # Optional: Click first search result if redirected to search page
#                 if "w/index.php?search=" in page.url:
#                     result = page.query_selector("ul.mw-search-results li a")
#                     if result:
#                         result.click()
#                         page.wait_for_load_state("networkidle")
#                         return jsonify({"result": f"Searched '{query}' on Wikipedia and opened first result."})
#                     else:
#                         return jsonify({"result": f"No search results found for '{query}'."})
#                 else:
#                     return jsonify({"result": f"Searched and landed directly on page for '{query}'."})

#             return jsonify({"result": "Command not recognized."})

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": traceback.format_exc()})


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)

## MILESTONE-1 ENDS ##

from flask import Flask, request, jsonify
from chrome_controller import ChromeController
import json
import time


app = Flask(__name__)

# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     print("Command received:", command)

#     try:
#         browser = ChromeController()

#         # EXAMPLE: "search for artificial intelligence on wikipedia"
#         if "wikipedia" in command and "search for" in command:
#             query = command.split("search for")[-1].split("on wikipedia")[0].strip()
#             browser.navigate_to(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
#             return jsonify({"result": f"Opened Wikipedia page for '{query}'."})

#         return jsonify({"result": "Command not recognized."})

#     except Exception as e:
#         return jsonify({"error": str(e)})

# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 const title = document.querySelector('h1')?.innerText;

#                 // Get all visible <p> elements under the content section
#                 const paragraphs = Array.from(document.querySelectorAll('#mw-content-text p'))
#                     .map(p => p.innerText)
#                     .filter(text => text.trim().length > 0)
#                     .slice(0, 3);  // limit to first 3 meaningful paragraphs

#                 return JSON.stringify({ title, paragraphs });
#             })()
#         """)
#         parsed = json.loads(result)
#         clean = json.loads(parsed["result"]["result"]["value"])
#         return jsonify(clean)
#     except Exception as e:
#         return jsonify({"error": str(e)})

# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 const title = document.querySelector('h1')?.innerText;

#                 // Get all visible <p> elements under the content section
#                 const paragraphs = Array.from(document.querySelectorAll('#mw-content-text p'))
#                     .map(p => p.innerText)
#                     .filter(text => text.trim().length > 0)
#                     .slice(0, 3);  // limit to first 3 meaningful paragraphs

#                 return JSON.stringify({ title, paragraphs });
#             })()
#         """)
#         parsed = json.loads(result)
#         clean = json.loads(parsed["result"]["result"]["value"])
#         return jsonify(clean)
#     except Exception as e:
#         return jsonify({"error": str(e)})

#------------uncomment-----------------
@app.route("/interact", methods=["POST"])
def interact():
    data = request.get_json()
    command = data.get("command", "").lower()
    print("Command received:", command)

    try:
        browser = ChromeController()

        # Handle "search for X on wikipedia"
        if "wikipedia" in command and "search for" in command:
            query = command.split("search for")[-1].split("on wikipedia")[0].strip()
            search_url = f"https://en.wikipedia.org/w/index.php?search={query.replace(' ', '+')}"
            browser.navigate_to(search_url)

            time.sleep(3)

            # Click on the first search result if it's a search results page
            browser.evaluate_js("""
                (() => {
                    const firstLink = document.querySelector('.mw-search-result-heading a');
                    if (firstLink) firstLink.click();
                })();
            """)
            
            time.sleep(3)

            return jsonify({"result": f"Opened Wikipedia article for '{query}'."})


        # Handle generic open command like "open linkedin", "open wikipedia"
        elif command.startswith("open "):
            domain = command.replace("open ", "").strip()
            if not domain.startswith("http"):
                domain = f"https://{domain}.com"
            browser.navigate_to(domain)
            return jsonify({"result": f"Opened '{domain}' in browser."})

        elif "get reviews of" in command:
            series = command.split("get reviews of")[-1].strip()
            search_query = f"{series} series reviews"

            browser.navigate_to(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            
            # Wait for results to load
            time.sleep(3)

            # Evaluate JS to scrape snippets
            result = browser.evaluate_js("""
                (() => {
                    const snippets = Array.from(document.querySelectorAll('div[data-content-feature="1"]'))
                    .map(e => e.innerText)
                    .filter(Boolean)
                    .slice(0, 5);  // top 5

                    return JSON.stringify(snippets);
                })()
            """)

            parsed = json.loads(result)
            
            # Print to terminal
            print("\n🔍 Top Reviews:\n")
            for idx, snippet in enumerate(parsed, 1):
                print(f"{idx}. {snippet}\n")

                return jsonify({"result": f"Fetched reviews for '{series}' and printed to console."})

        return jsonify({"result": "Command not recognized."})

    except Exception as e:
        return jsonify({"error": str(e)})



@app.route("/login_and_search", methods=["POST"])
def login_and_search():
    try:
        data = request.get_json()
        browser = ChromeController()

        # Step 1: Go to login
        browser.navigate_to("https://www.linkedin.com/login")

        # Step 2: Fill login details
        browser.evaluate_js(f'''
            document.querySelector("#username").value = "{data["username"]}";
            document.querySelector("#password").value = "{data["password"]}";
            document.querySelector("button[type=submit]").click();
        ''')

        time.sleep(5)  # wait for login

        # Step 3: Go to job search
        search_query = data["search"]
        browser.navigate_to(f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}")

        return jsonify({"result": f"Searched LinkedIn jobs for '{search_query}'."})
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

