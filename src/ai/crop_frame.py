from PIL import Image
from src.util.path import PROJECT_ROOT

def get_resolution_ratios(width, height):
    """
    Finds the measurement file and calculates the Workshop-to-Frame ratio.
    If the file is missing, raises an error with instructions.
    """
    config_dir = PROJECT_ROOT / "src" / "config" / "resolution_measures"
    measure_file = config_dir / f"small_facility_{width}x{height}.bmp"
    
    if not measure_file.exists():
        # Raise descriptive error instead of returning defaults
        raise FileNotFoundError(
            f"\n[Error] Missing resolution measurement for {width}x{height}.\n"
            f"To fix this, follow these steps:\n"
            f"1. Run 'python -m src.tools.measure_resolution' while playing at {width}x{height}.\n"
            f"2. Locate the new file at: {measure_file}\n"
            f"3. Open the file in an editor and crop it EXACTLY to the workshop panel boundaries.\n"
            f"4. Save and overwrite the file, then restart your script."
        )

    with Image.open(measure_file) as m_img:
        m_w, m_h = m_img.size
        # Ratio of the Workshop panel relative to the full frame it came from
        return m_w / width, m_h / height

def crop_frame(img: Image.Image, target_res=(1920, 1200), h_pos='left', v_pos='top'):
    """
    Crops the frame so the Workshop's relative size matches the 1920x1200 baseline.
    """
    curr_w, curr_h = img.size
    target_w, target_h = target_res

    # 1. Get ratios for both resolutions. 
    # This will raise an error if either the baseline or current res is unmeasured.
    t_ratio_w, t_ratio_h = get_resolution_ratios(target_w, target_h)
    c_ratio_w, c_ratio_h = get_resolution_ratios(curr_w, curr_h)

    # 2. Calculate the scaling factor needed to align the two
    # Ensures the workshop occupies the same proportional area as the training data
    scale_w = c_ratio_w / t_ratio_w
    scale_h = c_ratio_h / t_ratio_h

    # 3. Determine new dimensions for the crop
    new_w = int(curr_w * scale_w)
    new_h = int(curr_h * scale_h)

    # 4. Apply Positional Anchors
    # Horizontal
    if h_pos == 'left':
        left = 0
    elif h_pos == 'right':
        left = curr_w - new_w
    else: # center
        left = (curr_w - new_w) // 2

    # Vertical
    if v_pos == 'top':
        top = 0
    elif v_pos == 'bottom':
        top = curr_h - new_h
    else: # center
        top = (curr_h - new_h) // 2

    # Ensure crop dimensions do not exceed image boundaries
    return img.crop((left, top, min(left + new_w, curr_w), min(top + new_h, curr_h)))