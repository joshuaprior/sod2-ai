def crop(self, x1: int, y1: int, x2: int, y2: int) -> "Img":
    """ Returns a 'view' by default (shares memory with original). """
    data = self._data[y1:y2, x1:x2]
    return Img(data)