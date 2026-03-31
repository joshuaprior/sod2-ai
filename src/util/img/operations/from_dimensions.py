@classmethod
def from_dimensions(cls, width: int, height: int) -> "Img":
    """ Creates a new Img with the given dimensions. """
    data = np.full((height, width, 3), (0, 0, 0), dtype=np.uint8)
    return cls(data)