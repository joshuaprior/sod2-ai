import numpy as np
import random
from tqdm import tqdm
from PIL import Image
from src.ai.synthetic_data.frame import Frame
from src.ai.synthetic_data.menus.get_menu import get_menu
from src.ai.synthetic_data.menus.menus import Menu
from src.util.path import SRC_PATH, DATA_PATH
from src.util.bmp import save_bmp

# --- Configuration & Assets ---
BG_FILES = [
    "sod2_205339_215625.bmp", "sod2_205359_644540.bmp", "sod2_205415_404741.bmp",
    "sod2_205456_706267.bmp", "sod2_205526_157887.bmp", "sod2_205555_223478.bmp",
    "sod2_212034_526575.bmp", "sod2_212159_112947.bmp", "sod2_212237_122815.bmp",
    "sod2_212421_583725.bmp", "sod2_212436_437910.bmp", "sod2_212442_778090.bmp"
]

_BACKGROUND_CACHE = {}

def get_random_background():
    """Selects a random background, upscales it to 4x once, and caches it."""
    fname = random.choice(BG_FILES)
    if fname not in _BACKGROUND_CACHE:
        bg_path = SRC_PATH / "ai" / "synthetic_data" / "backgrounds" / fname
        if not bg_path.exists():
            print(f"Warning: Background {fname} not found. Using black.")
            black_bg = Image.new('RGB', (2560 * 4, 1440 * 4), (0, 0, 0))
            _BACKGROUND_CACHE[fname] = black_bg
        else:
            img = Image.open(bg_path).convert("RGB")
            scaled_bg = img.resize((2560 * 4, 1440 * 4), Image.Resampling.NEAREST)
            _BACKGROUND_CACHE[fname] = scaled_bg
            
    return _BACKGROUND_CACHE[fname]

def generate_set(count: int, folder_name: str, force_workshop_selected: bool = False):
    """
    Generates frames with randomized icon presence to prevent overfitting.
    """
    output_dir = DATA_PATH / "training_data" / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {count} images in {output_dir}...")

    for i in tqdm(range(count)):
        bg_asset = get_random_background()
        frame = Frame(bg_asset)
        
        # 1. Determine selection target
        selected_target = None
        if force_workshop_selected:
            selected_target = Menu.WORKSHOP
        else:
            # For 'not_workshop', 50% chance of someone else, 50% chance of NO selection
            if random.random() < 0.5:
                non_workshop_items = [m for m in Menu if m != Menu.WORKSHOP]
                selected_target = random.choice(non_workshop_items)

        # 2. Add facilities with 'Sparse Presence' logic
        for menu_type in Menu:
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