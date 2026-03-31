def paste(self, img: "Img", x: int, y: int):
    """
    Pastes another Img into this one at the given (x, y) coordinates.
    This is an opaque copy (no alpha blending).
    """
    w, h = img.size
    self._data[y : y + h, x : x + w] = img.raw_data
