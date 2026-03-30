import cv2
import numpy as np

def resize(img: np.ndarray, target_res: tuple[int, int]) -> np.ndarray:
    """Resizes the image to the target resolution."""
    current_h, current_w = img.shape[:2]
    target_w, target_h = target_res

    # Short-circuit if already at target resolution
    if (current_w, current_h) == (target_w, target_h):
        return img.copy()

    # Perform the resize
    return cv2.resize(
        img, 
        (target_w, target_h), 
        interpolation=cv2.INTER_AREA if (target_w < current_w) else cv2.INTER_CUBIC
    )