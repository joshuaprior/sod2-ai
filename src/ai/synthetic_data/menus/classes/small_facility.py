from PIL import Image
from ..menu import Menu

'''
Selection Rect Details:
Width: 158px
Height: 203px
Border Width: 7px
Corner Radius: 12px

Sample Position: (1331, 308)
'''

class SmallFacility(Menu):
    """Implementation of a small facility menu item."""
    WIDTH = 156
    HEIGHT = 202

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