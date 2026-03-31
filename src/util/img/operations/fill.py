def fill(self, color: tuple[int, int, int]):
    """ Fills the entire image with the specified RGB color. """
    self._data[:] = color