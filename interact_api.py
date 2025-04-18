# interact_api.py
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from browser_controller import BrowserController

# app = FastAPI()
# browser = BrowserController()

# class Command(BaseModel):
#     command: str

# @app.post("/interact")
# async def interact(cmd: Command):

#####################-----------below is working code ###########################
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"hello": "world"}

# class Command(BaseModel):
#     command: str

# @app.post("/interact")
# async def interact(cmd: Command):
#     return {"received_command": cmd.command}

### for ✅ Interact API that accepts natural language commands
### ✅ Properly handle error scenarios with clear messages

# def parse_commands(command: str):
#     if "login" in command:
#         return {"action":"login","site": "gmail.com"}
#     elif "search for" in command:
#         return {"action":"search","query":command.split("search for")[-1].strip()}
import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from pydantic import BaseModel
from browser_controller import BrowserController

app = FastAPI()
browser = BrowserController()

class Command(BaseModel):
    command: str

@app.post("/interact")
def interact(cmd: Command):
    return {"result": browser.handle(cmd.command)}
