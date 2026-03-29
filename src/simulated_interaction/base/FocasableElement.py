
from src.util import Img, Rect

class FocasableElement:
    def __init__(self, id: str, rect: Rect):
        self.id = id
        self.rect = rect
        self._selection = Rect(*rect.position, 0, 0)
        self._icon = None

    @property
    def selection(self) -> Rect:
        return self._selection + self.rect.position

    @property
    def icon(self) -> Rect|None:
        if self._icon is None:
            return None
        return self._icon + self.rect.position