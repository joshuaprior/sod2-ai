from PIL import Image
from src.util.path import ASSETS_PATH

def quartic_blending(input_range: tuple[int, int], value_range: tuple[int, int]) -> tuple[int, int]:
    a, c = input_range
    b, d = value_range
    def blend(x: int) -> int:
        y = (d - b) * (x - a)**4 / (c - a)**4 + b
        return round(y)
    return blend

def box_iterator(x1: int, y1: int, x2: int, y2: int):
    for x in range(x1, x2 + 1):
        yield (x, y1)
        yield (x, y2)
    for y in range(y1 + 1, y2):
        yield (x1, y)
        yield (x2, y)

def run():
    """Processes the raw brown background into a SmallFacility asset."""
    ICONS = ASSETS_PATH / "synthetic_data" / "icons"
    input_path = ICONS / "raw" / "background" / "background2.png"
    output_dir = ICONS / "facility" / "background"
    output_path = ICONS / "facility" / "background" / "small_facility_background.png"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Error: Raw background not found at {input_path}")
        return

    # 2. Resize to 121x119
    img = Image.open(input_path).convert("RGBA")
    img = img.resize((121, 119), Image.Resampling.LANCZOS)
    
    # 3. Set 1px outer border alpha to 0
    width, height = img.size
    pixels = img.load()

    inner_most_box = (58, 58, 62, 60)
    num_concentric_boxes = height // 2 - 1
    blend = quartic_blending((0, num_concentric_boxes), (0, 255))

    for i in range(num_concentric_boxes + 1):
        alpha = 255 - blend(i)
        x1 = inner_most_box[0] - i
        y1 = inner_most_box[1] - i
        x2 = inner_most_box[2] + i
        y2 = inner_most_box[3] + i 
        for x, y in box_iterator(x1, y1, x2, y2):
            r, g, b, a = pixels[x, y]
            pixels[x, y] = (r, g, b, alpha)
    
    # 4. Paste into target resolution (158x203)
    # This matches the WIDTH/HEIGHT of SmallFacility in your classes
    canvas_w, canvas_h = 158, 203
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    # Calculate centering
    paste_x = (canvas_w - width) // 2 + 1
    paste_y = (canvas_h - height) // 2 - 24
    
    # Use img as the mask to preserve the transparent border
    canvas.paste(img, (paste_x, paste_y), mask=img)

    # 5. Save
    canvas.save(output_path)
    print(f"Successfully generated background: {output_path}")

if __name__ == "__main__":
    run()