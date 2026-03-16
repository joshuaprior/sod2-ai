from PIL import Image, ImageDraw
from src.util.path import ASSETS_PATH

def generate_selection_rects():
    """
    Generates a series of white selection rectangles at opacities from 80% to 100%.
    Assets are rendered at 4x then downsampled to 1x for high-quality antialiasing.
    """
    # 1. Configuration (Target 1x based on your alignment test)
    T_WIDTH, T_HEIGHT = 158, 203
    T_BORDER = 7
    T_RADIUS = 12
    SCALE = 4
    
    # 2. Super-Resolution Dimensions (4x)
    S_WIDTH = T_WIDTH * SCALE
    S_HEIGHT = T_HEIGHT * SCALE
    S_BORDER = T_BORDER * SCALE
    S_RADIUS = T_RADIUS * SCALE

    # Define Output Directory
    output_dir = ASSETS_PATH / "synthetic_data" / "selection"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating assets in: {output_dir}")

    # 3. Opacity Loop (80% to 100%)
    for percent in range(80, 101):
        # Calculate alpha value (0-255)
        alpha = int(255 * (percent / 100))
        
        # Create a Transparent Canvas at 4x
        img = Image.new("RGBA", (S_WIDTH, S_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw the Rounded Rectangle at 4x
        # White color: (255, 255, 255)
        draw.rounded_rectangle(
            [0, 0, S_WIDTH, S_HEIGHT],
            radius=S_RADIUS,
            outline=(255, 255, 255, alpha),
            width=S_BORDER
        )

        # 4. Downsample to 1x
        final_rect = img.resize((T_WIDTH, T_HEIGHT), Image.Resampling.LANCZOS)

        # 5. Save with descriptive name
        file_name = f"selection_rect_small_facility_{percent}.png"
        final_rect.save(output_dir / file_name)
        print(f"  - Created: {file_name} (Alpha: {alpha})")

def run():
    print("--- Starting Selection Asset Generation ---")
    generate_selection_rects()
    print("--- Batch Generation Complete ---")

if __name__ == "__main__":
    run()