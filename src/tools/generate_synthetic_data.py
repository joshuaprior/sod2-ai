import numpy as np
from PIL import Image, ImageDraw
from src.util.path import SRC_PATH, DATA_PATH
from src.util.bmp import save_bmp

# --- Configuration (2560x1440 Baseline) ---
TARGET_RES = (2560, 1440)
SCALE_FACTOR = 4
SUPER_RES = (TARGET_RES[0] * SCALE_FACTOR, TARGET_RES[1] * SCALE_FACTOR)

# Precise White (Outer) Rectangle Config
WHITE_TARGET_SIZE = (156, 202) 
WHITE_TARGET_OFFSET = 14
WHITE_TARGET_RADIUS = 12
WHITE_TARGET_WIDTH = 6

def run():
    print(f"--- Synthetic Data Generator: Phase 9 (Final Geometry) ---")
    
    # 1. Create the Large Canvas (Pure Black)
    img_large = Image.new('RGB', SUPER_RES, (0, 0, 0))
    draw = ImageDraw.Draw(img_large)

    # 2. Load the Workshop Icon
    icon_path = SRC_PATH / "ai" / "synthetic_data" / "facility_icons" / "workshop.bmp"
    if not icon_path.exists():
        print(f"Error: Icon not found at {icon_path}")
        return
    workshop_icon = Image.open(icon_path).convert("RGBA")
    
    # 3. Calculate TOTAL Slot Dimensions for Centering
    # Based on the 156x202 white box
    s_box_w = WHITE_TARGET_SIZE[0] * SCALE_FACTOR
    s_box_h = WHITE_TARGET_SIZE[1] * SCALE_FACTOR
    
    canvas_cx, canvas_cy = SUPER_RES[0] // 2, SUPER_RES[1] // 2
    
    # White Box Coordinates
    white_rect_coords = [
        canvas_cx - (s_box_w // 2),
        canvas_cy - (s_box_h // 2),
        canvas_cx + (s_box_w // 2),
        canvas_cy + (s_box_h // 2)
    ]
    
    # 4. Position the ICON relative to White Box (14px offset)
    icon_x = white_rect_coords[0] + (WHITE_TARGET_OFFSET * SCALE_FACTOR)
    icon_y = white_rect_coords[1] + (WHITE_TARGET_OFFSET * SCALE_FACTOR)

    # 5. Draw the WHITE Selection Rectangle
    draw.rounded_rectangle(
        white_rect_coords,
        radius=WHITE_TARGET_RADIUS * SCALE_FACTOR,
        outline=(255, 255, 255), # Pure White
        width=WHITE_TARGET_WIDTH * SCALE_FACTOR
    )

    # 6. Render the Icon onto the 4x Canvas
    img_large.paste(workshop_icon, (int(icon_x), int(icon_y)), workshop_icon)

    # 7. Downsample
    print("Performing final downsample for Phase 9...")
    img_final = img_large.resize(TARGET_RES, Image.Resampling.LANCZOS)

    # 8. Save
    output_path = DATA_PATH / "debug_supersampling_test.bmp"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_bmp(np.array(img_final), output_path)

    print(f"Test frame saved to: {output_path}")
    print(f"Cleanup complete: Blue rectangle removed.")

if __name__ == "__main__":
    run()