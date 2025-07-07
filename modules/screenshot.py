import pyscreenshot as ImageGrab
import os
import datetime
import time

class Screenshot:
    def __init__(self, save_dir):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        print(f"Screenshot module initialized. Screenshots will be saved temporarily to: {self.save_dir}")

    def take_screenshot(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") # Add microseconds
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.save_dir, filename)

            # Try to grab the screen. pyscreenshot will try available backends.
            # Make sure you have 'mss' or 'Pillow' installed for macOS.
            im = ImageGrab.grab(bbox=None, childprocess=False) # bbox=None takes full screen
            im.save(filepath)
            return filepath
        except ImageGrab.exceptions.FailedBackendError as e:
            print(f"Error taking screenshot (backend issue): {e}")
            print("Please ensure you have a suitable backend installed for pyscreenshot (e.g., 'mss' or 'Pillow' for macOS).")
            return None
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None