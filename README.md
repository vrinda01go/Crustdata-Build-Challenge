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
python flask_api.py
```
## To interact with the agent, run 
``` powershell
  Invoke-WebRequest -Uri "http://localhost:8000/interact" `
 -Method POST `
 -Headers @{ "Content-Type" = "application/json" } `
 -Body '{ "command": "search for artificial intelligence on wikipedia" }'
