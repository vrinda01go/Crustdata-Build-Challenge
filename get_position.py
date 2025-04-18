import pyautogui
import time

def capture(label):
    print(f"➡️ Move your mouse to the {label}... You have 5 seconds.")
    time.sleep(5)
    pos = pyautogui.position()
    print(f"✅ {label} at: {pos}")
    return pos

if __name__ == "__main__":
    print("🎯 Coordinate Capturing Started")

    login_button = capture("Login Option (e.g., 'Log In' nav button)")
    username = capture("Username Field")
    password = capture("Password Field")
    submit = capture("Login Button or hit Enter")

    print("\n📝 Final Coordinates Summary:")
    print(f"Login Option    : {login_button}")
    print(f"Username Field  : {username}")
    print(f"Password Field  : {password}")
    print(f"Login Button    : {submit}")

    print("\n✅ Copy these into your automation script.")
