import pyautogui
import time

def native_login_flow():
    print("⏳ Switch to Chrome and get ready... starting in 5 seconds")
    time.sleep(5)

    # Step 1: Click login option
    pyautogui.click(x=1759, y=174)
    time.sleep(1)  # Let login form load

    # Step 2: Click and type username
    pyautogui.click(x=865, y=692)
    time.sleep(0.5)
    pyautogui.write("fakeuser123", interval=0.1)

    # Step 3: Click and type password
    pyautogui.click(x=846, y=805)
    time.sleep(0.5)
    pyautogui.write("fakepassword", interval=0.1)

    # Step 4: Click login or press enter
    pyautogui.click(x=936, y=945)
    # or use: pyautogui.press("enter")

if __name__ == "__main__":
    native_login_flow()
