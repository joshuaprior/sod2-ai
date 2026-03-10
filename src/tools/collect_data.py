from pathlib import Path
import keyboard
from datetime import datetime
from src.util.path import DATA_PATH
from src.io.capture_frame import capture_frame
from src.util.bmp import save_bmp

# --- Configuration ---
RAW_DATA_DIR = DATA_PATH / "raw_screenshots"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def on_hotkey():
    print("Attempting capture...")
    frame = capture_frame()

    if frame is not None:
        timestamp = datetime.now().strftime("%H%M%S_%f")
        file_path = RAW_DATA_DIR / f"sod2_{timestamp}.bmp"
        
        # cv2 requires strings for paths, so we convert the Path object
        save_bmp(frame, file_path)
        print(f"Captured: {file_path}")
    else:
        print("Capture failed. Is the game window 'StateOfDecay2 ' open?")

def run():
    print("Press F9 to Capture. Press Esc to Exit.")
    
    keyboard.add_hotkey('f9', on_hotkey)
    
    # Block until Esc is pressed
    keyboard.wait('esc')

if __name__ == "__main__":
    run()