# Crustdata-Build-Challenge

# Milestone 1

## Overview
This is a natural language browser automation API using Flask and Playwright.

## Features (Milestone 1)
- POST `/interact` with natural commands like:
  - `search for artificial intelligence on Wikipedia`
- The app will:
  - Launch a browser
  - Navigate to Wikipedia
  - Perform a search
  - Open the first result

## How to Run

```bash
pip install -r requirements.txt
python flask_api_1.py
```
## To interact with the agent, run 
``` powershell
  Invoke-WebRequest -Uri "http://localhost:8000/interact" `
 -Method POST `
 -Headers @{ "Content-Type" = "application/json" } `
 -Body '{ "command": "search for artificial intelligence on wikipedia" }'
```
# Milestone 2: Advanced Browser Integration

## Overview

This milestone demonstrates advanced browser automation capabilities using native Chrome integration via the Chrome DevTools Protocol. It builds on Milestone 1 by adding direct control of a locally installed browser, proxy support, browser extension integration, and a fully automated user journey with structured data extraction.

---

## Features Implemented

### 🔗 Level 1 Recap
-Implement an interact API that accepts natural language commands to control browser actions
-Properly handle common error scenarios with clear error messages
-Successfully demonstrate one complete flow with the interact API:
-Log into a popular website
-Perform a search with user-specified keywords
-Navigate through search results and interact with a specific result item


---

### 🚀 Milestone 2 – Advanced Features

| Feature                         | Status | Notes |
|--------------------------------|--------|-------|
| **Native Chrome control**      | ✅     | Using DevTools Protocol, not headless |
| **Interact API upgrade**       | ✅     | Supports user commands for Wikipedia, Google, LinkedIn |
| **Structured data extraction** | ✅     | Clean output from Wikipedia, Google, etc. |
| **Proxy configuration**        | ✅     | Verified with httpbin and mitmproxy |
| **Browser extension support**  | ✅     | Spotisush loaded via `--load-extension` |
| **User login + search flow**   | ✅     | Automates LinkedIn login and job search |
| **Console-based verification** | ✅     | All actions print logs to terminal for traceability |

---

## 🧪 Demonstration Flow

### 🔌 Proxy Test
- Chrome launched with `--proxy-server="http://127.0.0.1:8089"`
- `/proxy_test` navigates to `https://httpbin.org/ip`
- Output shows public IP via proxy
- Validated with mitmproxy log trace

### 🧩 Extension Test
- Chrome launched with Spotisush
- Verified in `chrome://extensions/`
- Extension injects script on matching pages (e.g., `open.spotify.com`)
- Console logs confirm `content.js` loaded

# 🧠 Milestone 2: OS-Level AI Browser Automation Agent

This project implements a local AI agent that automates browser tasks natively—without using Selenium, Playwright, or Puppeteer. All interactions are performed via **OS-level APIs** using `pyautogui` and `pygetwindow`.

---

## 🚀 Features Covered

✅ Interact API using natural language  
✅ Structured data extraction from browser pages  
✅ Proxy support via Chrome flags  
✅ Chrome extension integration  
✅ Native typing, clicking, and navigation  
✅ Demonstrated login flows and Wikipedia scraping

---

## 📁 Project Structure

<pre> ``` ai_browser/ ├── automation_task.py # Utility functions for login, search, and proxy verification ├── flask_server.py # Main server for Interact, Extract, and Login APIs ├── launch_chrome.bat # Chrome launchers (normal and proxy modes) ``` </pre>

---

## 🔧 Prerequisites

- **Python** 3.10+ with the following packages:

```bash
pip install flask pyautogui pygetwindow pyperclip requests
```
Google Chrome installed at: C:\Program Files\Google\Chrome\Application\chrome.exe

Optional Chrome Extension:

Download and extract any local extension. This project demonstrates with one called spotisush, located at: C:\Users\workstation\Downloads\spotisush

## 🧑‍💻 Running the Agent
1. Activate Python Environment
   ```bash
   cd C:\Users\workstation\ai_browser
   \venv310\Scripts\activate
   ```
2. Launch Chrome: launch_chrome.bat file
   <pre lang="markdown"> ```bat @echo off start chrome ^ --remote-debugging-port=9222 ^ --remote-allow-origins=* ^ --user-data-dir="C:\Users\workstation\ai_browser\chrome_profile" ^ --load-extension="C:\Users\workstation\Downloads\spotisush" ^ --ignore-certificate-errors ^ --no-first-run ^ --no-default-browser-check ^ --disable-web-security ^ --disable-site-isolation-trials ^ "https://open.spotify.com" ``` </pre>

   ✅ This opens Chrome with the spotisush extension and the required debug flags.

   🌍 Proxy Mode (using MITMProxy or any HTTP proxy)
   

   


