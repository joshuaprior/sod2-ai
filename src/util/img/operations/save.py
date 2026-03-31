def save(self, path: Path):
    """
    Saves the image to disk. The format is determined by the 
    file extension in the path (.bmp, .png, etc.).
    """
    # Convert internal RGB to BGR before saving
    data = cv2.cvtColor(self._data, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(path), data)