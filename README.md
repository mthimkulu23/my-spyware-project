# Local System Monitoring Tool (Educational/Local Use)

This project demonstrates a basic local system monitoring tool implemented in Python. It includes modules for keylogging, periodic screen capturing, and file system activity monitoring. All collected data is stored **locally** on the system where the tool is run and **is NOT exfiltrated to any remote server.**

**Purpose:** This tool is designed for educational purposes, for personal local monitoring on systems where explicit consent has been granted, or for testing security measures in a controlled environment. It explicitly avoids remote data transmission.

## Features

* **Keylogger:** Records keystrokes and saves them to a local log file.

* **Screenshot Capture:** Periodically takes screenshots of the desktop and saves them to a local directory.

* **File Monitor:** Monitors specified directories for file creation, deletion, modification, and movement, logging these events locally.

* **Local Data Storage:** All collected data (keylogs, screenshots, file change logs) is stored in a designated local `data/` directory.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.8+ (recommended)

* `pip` (Python package installer)

### Setup

1.  **Clone the Repository (if applicable) or navigate to your project folder:**

    ```bash

    cd /path/to/my-spyware-project
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**

    It's good practice to use a virtual environment to manage project dependencies.

    ```bash

    python3 -m venv .venv

    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required Python packages using `pip`.

    ```bash

    pip install -r requirements.txt

    # Or, if you don't have requirements.txt updated:

    # pip install pynput pyscreenshot mss watchdog
    ```

4.  **Create Monitored Directories:**

    The file monitor watches specific directories. Ensure these exist on your system.

    (Update `/Users/damacm1126` to your actual user path if different)

    ```bash
    mkdir -p /Users/damacm1126/test_docs

    mkdir -p /Users/damacm1126/my_projects
    ```
    You can also modify the `MONITORED_DIRECTORIES` list in `main.py` to target different paths.

5.  **<span style="color:red">**CRITICAL: macOS Accessibility Permissions**</span>**

    If you are running this tool on **macOS**, the keylogger and screenshot modules require special Accessibility permissions due to macOS's strong security measures. **The tool WILL NOT function correctly (keylogging and screenshots will fail) without these permissions.**

    You **MUST** manually grant permission:

    * Go to **System Settings** (or System Preferences on older macOS versions).

    * Navigate to **Privacy & Security**.

    * Scroll down the sidebar and click on **Accessibility**.

    * You will see a list of applications. If your Python executable is not listed, click the `+` button.
    
    * Browse to your virtual environment's Python executable. This is typically located at:
        `/<path_to_your_project>/.venv/bin/python`
        For example: `/Users/damacm1126/Documents/SPYWARE/my-spyware-project/.venv/bin/python`
    * Select this `python` executable and click "Open".
    * Once `python` is listed, **ensure the checkbox next to it is checked**. You might need to unlock the settings with your password.

## Running the Tool

Once all prerequisites and setup steps are completed, you can run the main script:

```bash

python main.py