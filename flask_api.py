from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)

@app.route("/interact", methods=["POST"])
def interact():
    data = request.get_json()
    command = data.get("command", "").lower()
    print("Received:", command)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            if "wikipedia" in command and "search for" in command:
                # Extract search query
                query = command.split("search for")[-1].split("on wikipedia")[0].strip()

                # 1. Go to Wikipedia
                page.goto("https://www.wikipedia.org")

                # 2. Fill the search box
                page.fill("input[name='search']", query)
                page.keyboard.press("Enter")

                # 3. Wait and click first result if it's a disambiguation or search list
                page.wait_for_load_state("networkidle")
                time.sleep(2)

                # Optional: Click first search result if redirected to search page
                if "w/index.php?search=" in page.url:
                    result = page.query_selector("ul.mw-search-results li a")
                    if result:
                        result.click()
                        page.wait_for_load_state("networkidle")
                        return jsonify({"result": f"Searched '{query}' on Wikipedia and opened first result."})
                    else:
                        return jsonify({"result": f"No search results found for '{query}'."})
                else:
                    return jsonify({"result": f"Searched and landed directly on page for '{query}'."})

            return jsonify({"result": "Command not recognized."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": traceback.format_exc()})


if __name__ == "__main__":
    app.run(port=8000, debug=True)

## MILESTONE-1 ENDS ##

## MILESTONE-2 STARTS ## 

# from flask import Flask, request, jsonify
# from chrome_controller import ChromeController
# import json
# import time


# app = Flask(__name__)

# # @app.route("/interact", methods=["POST"])
# # def interact():
# #     data = request.get_json()
# #     command = data.get("command", "").lower()
# #     print("Command received:", command)

# #     try:
# #         browser = ChromeController()

# #         # EXAMPLE: "search for artificial intelligence on wikipedia"
# #         if "wikipedia" in command and "search for" in command:
# #             query = command.split("search for")[-1].split("on wikipedia")[0].strip()
# #             browser.navigate_to(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
# #             return jsonify({"result": f"Opened Wikipedia page for '{query}'."})

# #         return jsonify({"result": "Command not recognized."})

# #     except Exception as e:
# #         return jsonify({"error": str(e)})

# # @app.route("/extract", methods=["POST"])
# # def extract():
# #     try:
# #         browser = ChromeController()
# #         result = browser.evaluate_js("""
# #             (() => {
# #                 const title = document.querySelector('h1')?.innerText;

# #                 // Get all visible <p> elements under the content section
# #                 const paragraphs = Array.from(document.querySelectorAll('#mw-content-text p'))
# #                     .map(p => p.innerText)
# #                     .filter(text => text.trim().length > 0)
# #                     .slice(0, 3);  // limit to first 3 meaningful paragraphs

# #                 return JSON.stringify({ title, paragraphs });
# #             })()
# #         """)
# #         parsed = json.loads(result)
# #         clean = json.loads(parsed["result"]["result"]["value"])
# #         return jsonify(clean)
# #     except Exception as e:
# #         return jsonify({"error": str(e)})

# # @app.route("/extract", methods=["POST"])
# # def extract():
# #     try:
# #         browser = ChromeController()
# #         result = browser.evaluate_js("""
# #             (() => {
# #                 const title = document.querySelector('h1')?.innerText;

# #                 // Get all visible <p> elements under the content section
# #                 const paragraphs = Array.from(document.querySelectorAll('#mw-content-text p'))
# #                     .map(p => p.innerText)
# #                     .filter(text => text.trim().length > 0)
# #                     .slice(0, 3);  // limit to first 3 meaningful paragraphs

# #                 return JSON.stringify({ title, paragraphs });
# #             })()
# #         """)
# #         parsed = json.loads(result)
# #         clean = json.loads(parsed["result"]["result"]["value"])
# #         return jsonify(clean)
# #     except Exception as e:
# #         return jsonify({"error": str(e)})
# @app.route("/interact", methods=["POST"])
# def interact():
#     data = request.get_json()
#     command = data.get("command", "").lower()
#     print("Command received:", command)

#     try:
#         browser = ChromeController()

#         # Handle "search for X on wikipedia"
#         if "wikipedia" in command and "search for" in command:
#             query = command.split("search for")[-1].split("on wikipedia")[0].strip()
#             browser.navigate_to(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
#             return jsonify({"result": f"Opened Wikipedia page for '{query}'."})

#         # Handle generic open command like "open linkedin", "open wikipedia"
#         elif command.startswith("open "):
#             domain = command.replace("open ", "").strip()
#             if not domain.startswith("http"):
#                 domain = f"https://{domain}.com"
#             browser.navigate_to(domain)
#             return jsonify({"result": f"Opened '{domain}' in browser."})

#         return jsonify({"result": "Command not recognized."})

#     except Exception as e:
#         return jsonify({"error": str(e)})



# @app.route("/login_and_search", methods=["POST"])
# def login_and_search():
#     try:
#         data = request.get_json()
#         browser = ChromeController()

#         # Step 1: Go to login
#         browser.navigate_to("https://www.linkedin.com/login")

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
# @app.route("/extract", methods=["POST"])
# def extract():
#     try:
#         browser = ChromeController()
#         result = browser.evaluate_js("""
#             (() => {
#                 const jobs = Array.from(document.querySelectorAll('.base-card')).map(card => {
#                     return {
#                         title: card.querySelector('h3')?.innerText || "",
#                         company: card.querySelector('.base-search-card__subtitle')?.innerText || "",
#                         location: card.querySelector('.job-search-card__location')?.innerText || ""
#                     };
#                 });
#                 return JSON.stringify(jobs);
#             })()
#         """)
#         return jsonify({"result": json.loads(result)})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
