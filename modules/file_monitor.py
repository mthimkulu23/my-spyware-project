import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, buffer_list):
        super().__init__()
        self.buffer = buffer_list
        print("ChangeHandler: Initialized.") # Added for clarity

    def on_created(self, event):
        if not event.is_directory:
            self.buffer.append(f"CREATED: {event.src_path}")
            # print(f"FileMonitor: Captured CREATED event: {event.src_path}") # For debugging

    def on_deleted(self, event):
        if not event.is_directory:
            self.buffer.append(f"DELETED: {event.src_path}")
            # print(f"FileMonitor: Captured DELETED event: {event.src_path}") # For debugging

    def on_modified(self, event):
        if not event.is_directory:
            self.buffer.append(f"MODIFIED: {event.src_path}")
            # print(f"FileMonitor: Captured MODIFIED event: {event.src_path}") # For debugging

    def on_moved(self, event):
        if not event.is_directory:
            self.buffer.append(f"MOVED: {event.src_path} to {event.dest_path}")
            # print(f"FileMonitor: Captured MOVED event: {event.src_path} to {event.dest_path}") # For debugging

class FileMonitor:
    def __init__(self, paths):
        self.paths = paths
        self.event_handler = None
        self.observer = None
        self.log_buffer = []
        self.scheduled_paths_count = 0 # Track how many paths were successfully scheduled
        print("FileMonitor: Initialized.")

    def start(self):
        self.observer = Observer()
        self.event_handler = ChangeHandler(self.log_buffer)

        for path in self.paths:
            if os.path.isdir(path):
                self.observer.schedule(self.event_handler, path, recursive=True)
                self.scheduled_paths_count += 1
                print(f"FileMonitor: Scheduled monitoring for existing directory: {path}")
            else:
                print(f"FileMonitor: Warning: Path '{path}' is not a directory or does not exist. Skipping monitoring.")

        # --- FIX START ---
        # Remove the incorrect if self.observer.emit_event(None): check
        if self.scheduled_paths_count > 0: # Only start observer if at least one path was scheduled
            self.observer.start()
            print("FileMonitor: Monitoring started with observer.")
        else:
            print("FileMonitor: No valid directories to monitor were scheduled. Observer not started.")
        # --- FIX END ---

    def stop(self):
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join(timeout=5)
            print("FileMonitor: Monitoring stopped.")

    def get_logs(self):
        """Returns the current accumulated file change logs as a string."""
        logs = "\n".join(self.log_buffer)
        return logs

    def clear_logs(self):
        """Clears the internal log buffer after it has been collected."""
        self.log_buffer = []
        # print("FileMonitor: Internal logs cleared.") # Commented out to reduce verbose output