import numpy as np
import random
from src.ai.synthetic_data.frame import Frame
from src.ai.synthetic_data.menus.get_menu import get_menu
from src.ai.synthetic_data.menus.menus import Menu
from src.util.path import DATA_PATH
from src.util.bmp import save_bmp

def run():
    print("--- Synthetic Data Tool: Random Position Test ---")
    frame = Frame()
    workshop = get_menu(Menu.WORKSHOP)
    workshop.set_selected(True)

    # Simple Randomization Loop
    max_attempts = 100
    placed = False

    for i in range(max_attempts):
        # Generate random coordinates (within target 2560x1440)
        # Note: We subtract width/height to increase chance of fitting
        rx = random.randint(0, 2560 - workshop.WIDTH)
        ry = random.randint(0, 1440 - workshop.HEIGHT)
        
        workshop.set_position(rx, ry)

        # Check if this random spot is valid
        is_valid, _ = frame.check_item(workshop)
        
        if is_valid:
            frame.add_item(workshop)
            print(f"Placed Workshop at ({rx}, {ry}) after {i+1} attempts.")
            placed = True
            break

    if not placed:
        print("Could not find a valid spot for the Workshop.")
        return

    # Render and Save
    final_image = frame.render()
    output_path = DATA_PATH / "random_test_frame.bmp"
    save_bmp(np.array(final_image), output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    run()