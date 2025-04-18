# automation_tasks.py
import pyautogui
import time
import pytesseract
from PIL import ImageGrab

# Optional: Set path if tesseract not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def open_wikipedia_and_search(query):
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyautogui.write("https://www.wikipedia.org", interval=0.05)
    pyautogui.press("enter")
    time.sleep(3)

    pyautogui.click(x=500, y=450)  # Adjust coordinates for search bar
    pyautogui.write(query, interval=0.05)
    pyautogui.press("enter")

def login_linkedin(email, password):
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyautogui.write("https://www.linkedin.com/login", interval=0.05)
    pyautogui.press("enter")
    time.sleep(5)

    pyautogui.click(x=850, y=500)  # Email field
    pyautogui.write(email, interval=0.05)

    pyautogui.click(x=850, y=560)  # Password field
    pyautogui.write(password, interval=0.05)

    pyautogui.click(x=860, y=610)  # Submit/login button

def search_jobs(query):
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write("https://www.linkedin.com/jobs", interval=0.05)
    pyautogui.press("enter")
    time.sleep(5)

    pyautogui.click(x=600, y=400)  # Click search bar
    pyautogui.write(query, interval=0.05)
    pyautogui.press("enter")

def get_reviews(query):
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write(f"https://www.google.com/search?q={query.replace(' ', '+')}+reviews", interval=0.05)
    pyautogui.press("enter")
    time.sleep(5)

def extract_visible_text():
    img = ImageGrab.grab(bbox=(100, 200, 1300, 1000))  # Adjust area
    text = pytesseract.image_to_string(img)
    return text

from PIL import ImageGrab

import pygetwindow as gw

def check_proxy_ip():
    chrome = None
    for w in gw.getWindowsWithTitle("Chrome"):
        if not w.isMinimized:
            chrome = w
            break
    if chrome:
        chrome.activate()
        time.sleep(1)

    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyautogui.write("https://httpbin.org/ip", interval=0.05)
    pyautogui.press("enter")
    time.sleep(5)

    screenshot = ImageGrab.grab()
    screenshot.save("proxy_test_result.png")
