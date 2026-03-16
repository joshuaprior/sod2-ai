from PIL import Image
from src.util.path import ASSETS_PATH
from ..menu import Menu

_SELECTION_CACHE = {}

def get_selection(opacity: int) -> Image.Image:
    """
    Returns a cached PIL Image of the selection rectangle for the 
    given opacity (80-100).
    """
    if opacity not in _SELECTION_CACHE:
        file_name = f"selection_rect_small_facility_{opacity}.png"
        path = ASSETS_PATH / "synthetic_data" / "selection" / file_name
        _SELECTION_CACHE[opacity] = Image.open(path).convert("RGBA")

    return _SELECTION_CACHE[opacity]

class SmallFacility(Menu):
    """Implementation of a small facility menu item."""
    WIDTH = 158
    HEIGHT = 203

    def __init__(self, icon_image: Image.Image):
        super().__init__()
        self.icon = icon_image

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """Returns the bounding box (x1, y1, x2, y2)."""
        x1, y1 = self.pos_x, self.pos_y
        x2, y2 = x1 + self.WIDTH, y1 + self.HEIGHT
        return (x1, y1, x2, y2)

    def render(self, canvas: Image.Image):
        """Renders the facility layers directly at the menu position."""
        pos = (self.pos_x, self.pos_y)

        # 1. Render the Icon
        canvas.paste(self.icon, pos, self.icon)

        # 2. Render Selection Overlay
        if self.selected:
            # Pulls the cached image from the selection factory
            rect = get_selection(self._selection_opacity)
            canvas.paste(rect, pos, rect)