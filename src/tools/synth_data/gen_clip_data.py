import random
import numpy as np
from PIL import Image
from tqdm import tqdm
from src.util.path import ASSETS_PATH, TRAINING_DATA_PATH
from src.util.bmp import save_bmp

# --- Configuration ---
BG_COLOR = (195, 195, 195)
SLOT_DIM = 15
CLIP_SOURCE_DIM = 21
IMG_SIZE = 224
SAMPLES_PER_CLASS = 1000

def get_slot_coordinates():
    """Calculates the top-left (x, y) for all 22 regions."""
    coords = []
    # Column 1 (Left): Slots 1-11
    for i in range(11):
        coords.append((0, 49 + (i * 16)))
    # Column 2 (Right): Slots 12-22
    for i in range(11):
        coords.append((16, 49 + (i * 16)))
    return coords

def load_clips(folder_name):
    """Loads all clips from a directory into a list of PIL Images."""
    path = ASSETS_PATH / "synthetic_data" / "clips" / folder_name
    return [Image.open(f).convert("RGB") for f in path.glob("*.bmp")]

def create_stitched_image(active_count, selected_index, selected_clips, unselected_clips):
    """
    Creates one 224x224 image.
    selected_index: 0-21 for a specific slot, or -1 for 'all unselected'.
    """
    # Create the base canvas filled with the border color
    canvas = Image.new("RGB", (IMG_SIZE, IMG_SIZE), BG_COLOR)
    slot_coords = get_slot_coordinates()

    for i in range(active_count):
        # 1. Determine if this slot is selected
        is_selected = (i == selected_index)
        source_pool = selected_clips if is_selected else unselected_clips
        
        # 2. Pick a random clip and apply the 15x15 'jiggle' crop
        base_clip = random.choice(source_pool)
        off_x = random.randint(0, CLIP_SOURCE_DIM - SLOT_DIM)
        off_y = random.randint(0, CLIP_SOURCE_DIM - SLOT_DIM)
        
        # Crop the 15x15 region out of the 21x21 source
        final_clip = base_clip.crop((off_x, off_y, off_x + SLOT_DIM, off_y + SLOT_DIM))
        
        # 3. Paste into the designated region
        canvas.paste(final_clip, slot_coords[i])
        
    return canvas

def run():
    print("--- Starting Clip-Based Synthetic Generation ---")
    
    # Load assets
    s_clips = load_clips("selected")
    u_clips = load_clips("unselected")
    
    if not s_clips or not u_clips:
        print("Error: Could not find clips in assets directory.")
        return

    # Classes: slot_01_selected ... slot_22_selected + all_unselected
    classes = [f"slot_{i+1:02d}" for i in range(22)] + ["unselected"]

    for class_name in classes:
        class_dir = TRAINING_DATA_PATH / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine the target index for this class
        target_idx = -1 if class_name == "unselected" else int(class_name.split('_')[1]) - 1

        for i in tqdm(range(SAMPLES_PER_CLASS), desc=f"Generating {class_name}"):
            # Randomize number of active slots (1-22)
            # Ensure n is at least large enough to include the selected slot
            min_n = target_idx + 1 if target_idx != -1 else 1
            n = random.randint(min_n, 22)
            
            img = create_stitched_image(n, target_idx, s_clips, u_clips)
            
            output_path = class_dir / f"clip_synth_{i:04d}.bmp"
            save_bmp(np.array(img), output_path)

    print(f"\nSuccess! Training data generated in: {TRAINING_DATA_PATH}")

if __name__ == "__main__":
    run()