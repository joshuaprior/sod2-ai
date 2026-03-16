import numpy as np
from PIL import Image
from pathlib import Path
from src.ai.synthetic_data import Frame, get_menu, Menus
from src.util.bmp import save_bmp

def run():
    print("--- Testing Workshop Icon Alignment ---")
    
    # 1. Configuration
    # Coordinates verified from the previous selection rectangle test
    POS_X, POS_Y = 1331, 308
    
    # Path to the specific game screenshot you provided earlier
    source_path = Path(r"C:\Users\joshu\Desktop\dev\git\sod2-ai\data\raw_screenshots\sod2_141706_813434.bmp")
    
    if not source_path.exists():
        print(f"Error: Could not find source image at {source_path}")
        return

    # 2. Setup the Frame
    # Load the screenshot as the background
    background = Image.open(source_path).convert("RGB")
    frame = Frame(background)
    
    # 3. Setup the Menu Item
    # This uses the factory to load the Workshop with your new antialiased icon
    workshop = get_menu(Menus.WORKSHOP)
    workshop.position = (POS_X, POS_Y)
    
    # We will set selected to False for now to focus purely on the icon alignment
    workshop.selected = False
    
    # 4. Add to Frame and Render
    # check_item and add_item will validate that it fits within the 2560x1440 bounds
    if frame.check_item(workshop):
        frame.add_item(workshop)
    else:
        print("Warning: Workshop item failed boundary/overlap checks.")

    # Render the final composite image
    debug_image = frame.render()
    
    # 5. Save the result
    output_path = source_path.parent / f"debug_icon_alignment_{source_path.name}"
    save_bmp(np.array(debug_image), output_path)

    print(f"Success! Debug icon alignment image saved to: {output_path}")

if __name__ == "__main__":
    run()