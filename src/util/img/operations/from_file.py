@classmethod
def from_file(cls, path: Path) -> "Img":
    """
    Loads a BMP or PNG from disk into a NumPy RGB array.
    PNG alpha channels are discarded.
    """
    # cv2.imread loads BGR by default
    bgr_data = cv2.imread(str(path))
    
    if bgr_data is None:
        raise FileNotFoundError(f"Could not load image at {str(path)}")

    # Convert BGR to RGB
    data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2RGB)
    
    return cls(data)