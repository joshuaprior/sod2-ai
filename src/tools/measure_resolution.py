from src.io.capture_frame import capture_frame
from src.util.bmp import save_bmp
from src.util.path import PROJECT_ROOT

def run():
    print("--- Resolution Measurement Tool ---")
    
    # 1. Setup the config directory relative to Project Root
    config_dir = PROJECT_ROOT / "src" / "config" / "resolution_measures"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Capture the clean client frame (excludes window chrome)
    frame = capture_frame()
    
    if frame is not None:
        height, width, _ = frame.shape
        # Use filename to store resolution for easier parsing later
        filename = f"small_facility_{width}x{height}.bmp"
        output_path = config_dir / filename
        
        # 3. Save as standard BMP
        save_bmp(frame, output_path)
        
        print(f"Captured: {output_path}")
        print("\nINSTRUCTIONS:")
        print(f"1. Open '{filename}' in your editor.")
        print("2. Crop it EXACTLY to the boundaries of one small facility.")
        print("3. Save/Overwrite the file.")
        print("4. This will be used to calculate relative UI ratios.")
    else:
        print("Capture failed. Is the game window open?")

if __name__ == "__main__":
    run()