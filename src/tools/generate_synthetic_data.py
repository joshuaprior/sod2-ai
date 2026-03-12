import numpy as np
from src.ai.synthetic_data.frame import Frame
from src.ai.synthetic_data.menus.get_menu import get_menu
from src.ai.synthetic_data.menus.menus import MenuType
from src.util.path import DATA_PATH
from src.util.bmp import save_bmp

def run():
    print("--- Synthetic Data Tool: Manual Architecture Test ---")
    
    # 1. Initialize the high-level Frame (Handles 4x super-res and downsampling)
    frame = Frame()

    # 2. Use the Factory to create a Workshop facility
    # Position (0, 0) in 2560x1440 space. 
    # The class will handle scaling this to (0, 0) in 10240x5760 space.
    try:
        workshop = get_menu(
            menu_type=MenuType.WORKSHOP, 
            position=(0, 0), 
            selected=True
        )
        
        # 3. Add to frame (triggers the overlaps/contains validation)
        frame.add_item(workshop)
        print("Successfully added Workshop at (0, 0).")

    except ValueError as e:
        print(f"Validation Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return

    # 4. Render the final 2560x1440 image
    print("Rendering and downsampling...")
    final_image = frame.render()

    # 5. Save to disk
    output_path = DATA_PATH / "manual_test_frame.bmp"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert PIL to numpy for your bmp utility
    save_bmp(np.array(final_image), output_path)

    print(f"Test complete. Image saved to: {output_path}")

if __name__ == "__main__":
    run()