import numpy as np
from PIL import Image
from src.util.bmp import save_bmp

def points(bounds):
    """
    Iterates over all the points in the bounding box.
    """
    yield (bounds[0], bounds[1])
    yield (bounds[0], bounds[3])
    yield (bounds[2], bounds[1])
    yield (bounds[2], bounds[3])

def contains_point(bounds, point):
    """
    Checks if a point is containd within the bounding box.
    """
    x, y = point
    x1, y1, x2, y2 = bounds
    return x1 <= x <= x2 and y1 <= y <= y2

def contains_rect(bounds1, bounds2):
    """
    Checks if bounds1 completely contains bounds2.
    """
    for point in points(bounds2):
        if not contains_point(bounds1, point):
            return False
    
    return True

def overlaps(a, b):
    """
    Checks if two bounding boxes (x1, y1, x2, y2) overlap.
    """

    # These helpers check if rect a is completely to the left or above rect b
    is_left = lambda a, b: a[2] < b[0]
    is_above = lambda a, b: a[3] < b[1]

    return not (
            is_left(a, b) or
            is_left(b, a) or
            is_above(a, b) or
            is_above(b, a)
        )

class Frame:
    """
    Manages a 4x supersampled canvas, handles collision detection, 
    and renders added menu items.
    """
    
    # Internal Constants
    TARGET_W = 2560
    TARGET_H = 1440
    SCALE = 4
    
    # Derived Super Res Constants
    SUPER_W = TARGET_W * SCALE
    SUPER_H = TARGET_H * SCALE

    def __init__(self):
        self.items = []

    def get_bounds(self):
        """
        Returns the 4x scaled bounding box of the entire frame.
        :return: (x1, y1, x2, y2)
        """
        return (0, 0, self.SUPER_W, self.SUPER_H)
    
    def add_item(self, menu_item):
        """
        Validates and adds a menu item to the frame.
        """
        # 1. Check if completely contained within Frame bounds
        if not contains_rect(self.get_bounds(), menu_item.get_bounds()):
            raise ValueError(f"Validation Failed: Item at {menu_item.get_bounds()} is out of frame bounds.")

        # 2. Check for overlap with existing items
        for existing_item in self.items:
            if overlaps(menu_item.get_bounds(), existing_item.get_bounds()):
                raise ValueError("Validation Failed: New item overlaps with a previously added item.")

        # 3. Validation passed
        self.items.append(menu_item)

    def render(self) -> Image.Image:
        """
        Creates the 4x super-res image, renders all items, and downsamples.
        :return: PIL Image at 2560x1440
        """
        # Create pure black super-res canvas
        canvas = Image.new('RGB', (self.SUPER_W, self.SUPER_H), (0, 0, 0))

        # Render all menu items onto the super-res canvas
        for item in self.items:
            item.render(canvas)

        # Final downsample to target resolution
        return canvas.resize((self.TARGET_W, self.TARGET_H), Image.Resampling.LANCZOS)