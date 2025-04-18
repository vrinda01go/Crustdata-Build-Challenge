import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from playwright.sync_api import sync_playwright

class BrowserController:
    def handle(self, command: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            if "open instagram" in command.lower():
                page.goto("https://www.instagram.com")
                page.wait_for_timeout(5000)
                return "Instagram opened successfully."

            elif "search for" in command.lower():
                query = command.split("search for")[-1].strip()
                page.goto("https://duckduckgo.com")
                page.fill("input[name='q']", query)
                page.keyboard.press("Enter")
                page.wait_for_selector("a.result__a", timeout=10000)
                results = page.query_selector_all("a.result__a")
                if results:
                    results[0].click()
                    page.wait_for_timeout(5000)
                    return f"Searched for '{query}' and clicked first result."
                else:
                    return f"No results found for '{query}'."

            return "Command not recognized."
