import random
from abc import ABC, abstractmethod
from PIL import Image

class Menu(ABC):
    """Abstract Base Class for all menu elements."""

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self._selected = False
        self._selection_opacity = random.randint(80, 100)

    @property
    def position(self) -> tuple[int, int]:
         return (self.pos_x, self.pos_y)

    @position.setter
    def position(self, pos: tuple[int, int]):
        self.pos_x, self.pos_y = pos

    @property
    def selected(self) -> bool:
        return self._selected
    
    @selected.setter
    def selected(self, selected: bool):
        self._selected = selected

    @property
    @abstractmethod
    def bounds(self) -> tuple[int, int, int, int]:
        """Must return (x1, y1, x2, y2)"""
        pass

    @abstractmethod
    def render(self, canvas: Image.Image):
        """Must draw the component onto the provided PIL canvas"""
        pass