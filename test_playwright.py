import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Navigating to DuckDuckGo...")
        await page.goto("https://duckduckgo.com")

        print("Filling search box...")
        await page.fill("input[name='q']", "mismatched series reviews")


        print("Submitting search...")
        await page.press("input[name='q']", "Enter")

        print("Waiting for results...")
        await page.wait_for_selector("a.result__a", timeout=5000)

        print("Clicking first result...")
        await page.click("a.result__a")

        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(run())
