import numpy as np
from PIL import Image
import keyboard
from datetime import datetime

from src.util.path import DATA_PATH
from src.util.bmp import save_bmp
from src.io.capture_frame import capture_frame
from src.ai.crop_frame import crop_frame

def on_hotkey():
    print("Attempting test crop...")
    
    # 1. Capture the live frame (Standardized RGB)
    frame_rgb = capture_frame()
    
    if frame_rgb is not None:
        # 2. Convert to PIL for the crop utility
        img = Image.fromarray(frame_rgb)
        
        # 3. Apply the 16:9 Top-Left crop
        # This uses the same logic we established for the Workshop menu
        cropped_img = crop_frame(img)
        
        # 4. Save the result to the data directory with a timestamp
        timestamp = datetime.now().strftime("%H%M%S_%f")
        output_path = DATA_PATH / f"debug_test_crop_{timestamp}.bmp"
        
        # Convert back to numpy array for our save utility
        final_output = np.array(cropped_img)
        save_bmp(final_output, output_path)

        print(f"Captured: {output_path}")
        print(f"  - Original: {img.size}")
        print(f"  - Cropped: {cropped_img.size}")
    else:
        print("Capture failed. Is the game window open?")

def run():
    print("--- Crop Logic Tester ---")
    print("Press F9 to Capture Test Crop. Press Esc to Exit.")
    
    # Matches the hotkey logic from collect_data.py
    keyboard.add_hotkey('f9', on_hotkey)
    
    # Block until Esc is pressed
    keyboard.wait('esc')

if __name__ == "__main__":
    run()