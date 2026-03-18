import numpy as np
from tqdm import tqdm
from src.ai.synthetic_data import (
    Frame, 
    Background, 
    get_menu, 
    Menus, 
    compose_frame, 
    select_menu,
    unselect_menu
)
from src.util.path import TRAINING_DATA_PATH
from src.util.bmp import save_bmp

GEN_WORKSHOP_COUNT = 1000
GEN_NOT_WORKSHOP_COUNT = 1000

def generate_batch(count: int, label: str):
    """Generates and saves a specific number of frames for a given label."""
    output_dir = TRAINING_DATA_PATH / label
    output_dir.mkdir(parents=True, exist_ok=True)
    
    bg_provider = Background()

    workshop = get_menu(Menus.WORKSHOP)
    others = [get_menu(Menus.FIGHTING_GYM), get_menu(Menus.SHOOTING_RANGE)]
    
    print(f"Generating {count} frames for '{label}'...")
    
    for i in tqdm(range(count)):
        # 1. Determine items and selection based on label
        if label == "workshop":
            # Workshop is always present and always selected
            items = select_menu(workshop, others)
        else:
            # Workshop is unselected; other facilities might be selected
            items = unselect_menu(workshop, others)
            
        # 2. Composition
        # Grab a random background asset
        frame = Frame(bg_provider.get_background())
        
        # Randomize positions (non-overlapping)
        compose_frame(frame, items)
        
        # 3. Render
        image = frame.render()
        
        # 4. Save to the label-specific folder
        output_path = output_dir / f"synth_{i:04d}.bmp"
        save_bmp(np.array(image), output_path)

def run():
    print("--- Starting Synthetic Data Generation (Small Test Run) ---")
    
    # Generate frames where Workshop is the target
    generate_batch(GEN_WORKSHOP_COUNT, "workshop")
    
    # Generate frames where Workshop is NOT the target
    generate_batch(GEN_NOT_WORKSHOP_COUNT, "not_workshop")
    
    print(f"\nSuccess! {GEN_WORKSHOP_COUNT + GEN_NOT_WORKSHOP_COUNT} frames generated in: {TRAINING_DATA_PATH}")

if __name__ == "__main__":
    run()