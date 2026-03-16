import numpy as np
from PIL import Image
from src.ai.synthetic_data import (
    Frame, 
    Background, 
    get_menu, 
    Menus, 
    compose_frame, 
    select_menu
)
from src.util.path import DATA_PATH
from src.util.bmp import save_bmp

def run():
    print("--- Generating Single Test Frame (1x Logic) ---")
    
    # 1. Setup Providers
    background = Background()
    
    # 2. Prepare the Menus
    # We'll simulate a 'Workshop' labeled frame
    workshop = get_menu(Menus.WORKSHOP)
    others = [get_menu(Menus.FIGHTING_GYM), get_menu(Menus.SHOOTING_RANGE)]
    
    # Decide which ones render and set selection state
    # This uses your new 50/50 logic from select_menu.py
    items = select_menu(workshop, others)
    
    # 3. Composition
    # Grab a random background
    frame = Frame(background.get_background())
    
    # Randomize positions on the frame
    compose_frame(frame, items)
    
    # 4. Render and Save
    image = frame.render()
    
    output_path = DATA_PATH / "debug_test_frame.bmp"
    save_bmp(np.array(image), output_path)
    
    print(f"Success! Test frame saved to: {output_path}")
    print(f"Items rendered: {[type(i).__name__ for i in items]}")

if __name__ == "__main__":
    run()