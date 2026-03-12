from PIL import Image, ImageDraw

class SmallFacility:
    WIDTH = 156
    HEIGHT = 202
    BORDER_WIDTH = 6
    CORNER_RADIUS = 12
    ICON_OFFSET = 14
    SCALE = 4

    def __init__(self, icon_image: Image.Image, position: tuple, selected: bool = False):
        """
        :param icon_image: The PIL Image object pre-loaded by the factory
        """
        self.icon = icon_image
        self.pos_x, self.pos_y = position
        self.selected = selected

    def get_bounds(self):
        x1 = self.pos_x * self.SCALE
        y1 = self.pos_y * self.SCALE
        x2 = (self.pos_x + self.WIDTH) * self.SCALE
        y2 = (self.pos_y + self.HEIGHT) * self.SCALE
        return (x1, y1, x2, y2)

    def render(self, canvas: Image.Image):
        s_x1, s_y1, s_x2, s_y2 = self.get_bounds()
        
        if self.selected:
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle(
                [s_x1, s_y1, s_x2, s_y2],
                radius=self.CORNER_RADIUS * self.SCALE,
                outline=(255, 255, 255),
                width=self.BORDER_WIDTH * self.SCALE
            )

        canvas.paste(self.icon, (int(s_x1 + (self.ICON_OFFSET * self.SCALE)), 
                                int(s_y1 + (self.ICON_OFFSET * self.SCALE))), self.icon)