from src.util import Rect
from .FocasableElement import FocasableElement

class SmallFacility(FocasableElement):
    def __init__(self, id: str, rect: Rect):
        super().__init__(id, rect)
        self._selection = Rect(-6, -6, 14, 14)
        self._icon = Rect(9, 9, 53, 53)