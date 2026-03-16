import numpy as np
import random
from tqdm import tqdm
from PIL import Image
from src.ai.synthetic_data import Frame, Background, get_menu, Menus
from src.util.path import TRAINING_DATA_PATH, ASSETS_PATH
from src.util.bmp import save_bmp

# --- Configuration & Assets ---
_BACKGROUND_PROVIDER = Background()

def generate_set(count: int, folder_name: str, force_workshop_selected: bool = False):
    """
    Generates frames with randomized icon presence to prevent overfitting.
    """
    output_dir = TRAINING_DATA_PATH / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {count} images in {output_dir}...")

    for i in tqdm(range(count)):
        # Acquire a base background from the provider (2560x1440)
        base_bg = _BACKGROUND_PROVIDER.get_background()
        # Upscale to the frame's supersampled resolution (4x)
        bg_asset = base_bg.resize((Frame.SUPER_W, Frame.SUPER_H), Image.Resampling.NEAREST)
        frame = Frame(bg_asset)
        
        # 1. Determine selection target
        selected_target = None
        if force_workshop_selected:
            selected_target = Menus.WORKSHOP
        else:
            # For 'not_workshop', 50% chance of someone else, 50% chance of NO selection
            if random.random() < 0.5:
                non_workshop_items = [m for m in Menus if m != Menus.WORKSHOP]
                selected_target = random.choice(non_workshop_items)

        # 2. Add facilities with 'Sparse Presence' logic
        for menu_type in Menus:
            # Always include the target we want to highlight
            # Otherwise, only 50% chance to include other facilities
            if menu_type != selected_target and random.random() < 0.5:
                continue

            facility = get_menu(menu_type)
            facility.set_selected(menu_type == selected_target)
            
            # Find a valid non-overlapping spot
            placed = False
            for _ in range(500):
                rx = random.randint(0, 2560 - facility.WIDTH)
                ry = random.randint(0, 1440 - facility.HEIGHT)
                facility.set_position(rx, ry)
                
                is_valid, _ = frame.check_item(facility)
                if is_valid:
                    frame.add_item(facility)
                    placed = True
                    break
            
        # 3. Render and Downsample
        final_image = frame.render()
        save_bmp(np.array(final_image), output_dir / f"frame_{i:04d}.bmp")

def run():
    """Generate 1,000 sparse images per folder."""
    # Folders will now have varied icon counts, making the model work harder
    generate_set(1000, "workshop", force_workshop_selected=True)
    generate_set(1000, "not_workshop", force_workshop_selected=False)

    print("\nBatch generation complete.")

if __name__ == "__main__":
    run()