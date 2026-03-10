import cv2
from pathlib import Path

def save_bmp(frame, path: Path):
    """
    Standardizes saving RGB frames to disk as BMP.
    Handles RGB -> BGR conversion and Path-to-String casting.
    """
    # Convert RGB (standard) back to BGR (OpenCV disk format)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # cv2 requires strings for paths
    cv2.imwrite(str(path), frame_bgr)