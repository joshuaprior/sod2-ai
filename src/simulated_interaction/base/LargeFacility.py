from src.util import Rect
from .FocasableElement import FocasableElement

class LargeFacility(FocasableElement):
    def __init__(self, id: str, rect: Rect):
        super().__init__(id, rect)
        self._selection = Rect(-4, -6, 14, 14)
        self._icon = Rect(13, 12, 72, 72)