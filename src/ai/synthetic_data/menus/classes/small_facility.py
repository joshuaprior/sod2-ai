from PIL import Image, ImageDraw
from ..menu import Menu

class SmallFacility(Menu):
    WIDTH = 156
    HEIGHT = 202
    BORDER_WIDTH = 6
    CORNER_RADIUS = 12
    ICON_OFFSET = 14
    SCALE = 4

    def __init__(self, icon_image: Image.Image):
        # Call the Menu base class constructor
        super().__init__()
        self.icon = icon_image

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        x1 = self.pos_x * self.SCALE
        y1 = self.pos_y * self.SCALE
        x2 = (self.pos_x + self.WIDTH) * self.SCALE
        y2 = (self.pos_y + self.HEIGHT) * self.SCALE
        return (x1, y1, x2, y2)

    def render(self, canvas: Image.Image):
        s_x1, s_y1, s_x2, s_y2 = self.bounds
        
        # 1. Draw Selection Rectangle
        if self._selected:
            # Create a temporary transparent layer for the rectangle
            overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            s_border = self.BORDER_WIDTH * self.SCALE
            s_radius = self.CORNER_RADIUS * self.SCALE
            
            overlay_draw.rounded_rectangle(
                [s_x1, s_y1, s_x2, s_y2],
                radius=s_radius,
                outline=(255, 255, 255, self.opacity), # White with Random Alpha
                width=s_border
            )
            # Alpha composite the overlay onto the main canvas
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"))

        # 2. Paste Icon
        offset = self.ICON_OFFSET * self.SCALE
        canvas.paste(self.icon, (int(s_x1 + offset), int(s_y1 + offset)), self.icon)