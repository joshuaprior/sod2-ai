import numpy as np
from src.ai.synthetic_data.frame import Frame
from src.ai.synthetic_data.menus.get_menu import get_menu
from src.ai.synthetic_data.menus.menus import Menu
from src.util.path import DATA_PATH
from src.util.bmp import save_bmp

def run():
    frame = Frame()

    try:
        workshop = get_menu(
            menu=Menu.WORKSHOP, 
            position=(0, 0), 
            selected=True
        )
        frame.add_item(workshop)

    except ValueError as e:
        print(f"Validation Error: {e}")
        return

    final_image = frame.render()
    output_path = DATA_PATH / "manual_test_frame.bmp"
    save_bmp(np.array(final_image), output_path)
    print(f"Test complete. Image saved to: {output_path}")

if __name__ == "__main__":
    run()