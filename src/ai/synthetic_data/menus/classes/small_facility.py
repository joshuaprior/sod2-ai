from PIL import Image, ImageDraw

class SmallFacility:
    WIDTH = 156
    HEIGHT = 202
    BORDER_WIDTH = 6
    CORNER_RADIUS = 12
    ICON_OFFSET = 14
    SCALE = 4

    def __init__(self, icon_image: Image.Image):
        """
        Constructor now only takes the essential asset.
        Position and Selection state are handled via methods.
        """
        self.icon = icon_image
        self.pos_x = 0
        self.pos_y = 0
        self._selected = False

    def set_position(self, x: int, y: int):
        """Sets the target position in 2560x1440 space."""
        self.pos_x = x
        self.pos_y = y

    def set_selected(self, selected: bool):
        """Sets whether the selection highlight should be rendered."""
        self._selected = selected

    def get_selected(self) -> bool:
        """Returns the current selection state."""
        return self._selected

    def get_bounds(self):
        """Returns 4x scaled (x1, y1, x2, y2)."""
        x1 = self.pos_x * self.SCALE
        y1 = self.pos_y * self.SCALE
        x2 = (self.pos_x + self.WIDTH) * self.SCALE
        y2 = (self.pos_y + self.HEIGHT) * self.SCALE
        return (x1, y1, x2, y2)

    def render(self, canvas: Image.Image):
        s_x1, s_y1, s_x2, s_y2 = self.get_bounds()
        
        if self._selected:
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle(
                [s_x1, s_y1, s_x2, s_y2],
                radius=self.CORNER_RADIUS * self.SCALE,
                outline=(255, 255, 255),
                width=self.BORDER_WIDTH * self.SCALE
            )

        # Offset icon 14px (scaled) from the top-left of the box
        offset = self.ICON_OFFSET * self.SCALE
        canvas.paste(self.icon, (int(s_x1 + offset), int(s_y1 + offset)), self.icon)