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


