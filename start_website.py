# Imports and libraries required to run this
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

# Website URL 
WEBSITE_URL = "http://localhost:8501"
PROJECT_FOLDER = Path(__file__).resolve().parent

#A function that waits for Streamlit to respond before opening the website
def wait_for_website(attempts=60):
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(WEBSITE_URL, timeout=1):
                return True
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
    return False

# A function that has specific parameters to run the API.
def main():
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app"],
        cwd=PROJECT_FOLDER,
    )

    website_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "website.py",
            "--server.headless=true",
        ],
        cwd=PROJECT_FOLDER,
    )

    try:
        if wait_for_website():
            webbrowser.open(WEBSITE_URL)
        else:
            print(f"The website did not start in time. Try opening {WEBSITE_URL}")

        website_process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        website_process.terminate()
        try:
            website_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            website_process.kill()

        api_process.terminate()
        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()


if __name__ == "__main__":
    main()
