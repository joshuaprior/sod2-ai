import json
import uuid
from PIL import Image
from pathlib import Path
from src.util.path import SRC_PATH, DATA_PATH

# Change this path to process different images
#INPUT_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "sod2_093559_920812.bmp" # Fighting Gym
# INPUT_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "sod2_093601_564801.bmp" # Workshop
INPUT_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "sod2_205828_486755.bmp" # Shooting Range

def run():
    # 1. Setup Paths
    config_path = SRC_PATH / "ai" / "facilities.json"
    output_dir = DATA_PATH / "clips"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not INPUT_IMAGE_PATH.exists():
        print(f"Error: Input image not found at {INPUT_IMAGE_PATH}")
        return

    # 2. Load Config
    with open(config_path, "r") as f:
        config = json.load(f)

    # 3. Get Framing and Home Site Data
    # Targeting the 2560x1440 resolution block
    res_data = config.get("2560x1440")
    if not res_data:
        print("Error: No configuration found for 2560x1440 resolution.")
        return

    # Get the 'tip' clipping region [x1, y1, x2, y2]
    tip_coords = res_data["framing"]["small_facility"]["tip"]
    
    # Find the specific home site
    home_site = next((site for site in res_data["home_sites"] 
                      if site["class"] == "lundegaard_lumber_mill"), None)
    
    if not home_site:
        print("Error: Could not find home site 'lundegaard_lumber_mill' in config.")
        return

    # 4. Process Image
    print(f"Processing image: {INPUT_IMAGE_PATH.name}")
    full_img = Image.open(INPUT_IMAGE_PATH).convert("RGB")
    written_files = []

    for slot in home_site["slots"]:
        if slot["size"] == "small":
            # Offset the tip region by the slot's position
            offset_x, offset_y = slot["pos"]
            
            # final_clip = [x1 + offset, y1 + offset, x2 + offset, y2 + offset]
            clip_box = (
                tip_coords[0] + offset_x - 3,
                tip_coords[1] + offset_y - 3,
                tip_coords[2] + offset_x + 4,
                tip_coords[3] + offset_y + 4
            )

            # Extract the region
            clip = full_img.crop(clip_box)

            # Generate unique filename using UUID to prevent clobbering
            file_id = uuid.uuid4().hex[:8]
            file_name = f"clip_{home_site['class']}_{offset_x}_{offset_y}_{file_id}.bmp"
            save_path = output_dir / file_name
            
            # Save as BMP for lossless inspection
            clip.save(save_path)
            written_files.append(file_name)

    # 5. Report Results
    print(f"\nExtraction Complete!")
    print(f"Total clips extracted: {len(written_files)}")
    print("New files written to DATA_PATH/clips:")
    for f in written_files:
        print(f"  - {f}")

if __name__ == "__main__":
    run()