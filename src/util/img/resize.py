import cv2
from src.util import Img

def resize(img: Img, target_res: tuple[int, int]) -> None:
    """Resizes the image in-place to the target resolution."""
    current_h, current_w = img.raw_data.shape[:2]
    target_w, target_h = target_res

    # 2. Short-circuit if already at target resolution
    if (current_w, current_h) == (target_w, target_h):
        return

    # 3. Perform the resize
    img._data = cv2.resize(
        img._data, 
        (target_w, target_h), 
        interpolation=cv2.INTER_AREA if (target_w < current_w) else cv2.INTER_CUBIC
    )