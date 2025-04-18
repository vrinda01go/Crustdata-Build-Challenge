import subprocess
import platform
import os
import shutil

def get_chrome_path():
    system = platform.system()
    if system == "Windows":
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif system == "Darwin":  # macOS
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system == "Linux":
        return shutil.which("google-chrome") or shutil.which("chromium-browser")
    else:
        raise Exception("Unsupported OS")

def launch_chrome():
    chrome_path = get_chrome_path()
    user_data_dir = os.path.join(os.path.expanduser("~"), "ai_browser", "chrome_profile")
    extension_path = os.path.join(os.path.expanduser("~"), "Downloads", "spotisush")

    command = [
        chrome_path,
        "--remote-debugging-port=9222",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data_dir}",
        f"--load-extension={extension_path}",
        "--ignore-certificate-errors",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-web-security",
        "--disable-site-isolation-trials",
        "https://open.spotify.com"
    ]

    subprocess.Popen(command)

if __name__ == "__main__":
    launch_chrome()
