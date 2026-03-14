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
    TARGET_W = 2560
    TARGET_H = 1440
    SCALE = 4
    SUPER_W = TARGET_W * SCALE
    SUPER_H = TARGET_H * SCALE

    def __init__(self, background_image: Image.Image):
        """
        :param background_image: A pre-scaled (4x) PIL Image.
        """
        self.items = []
        # We start with a copy of the background instead of a black canvas
        self.background = background_image

    def get_bounds(self):
        return (0, 0, self.SUPER_W, self.SUPER_H)
    
    def check_item(self, menu_item):
        """
        Checks if a menu item can be added without actually adding it.
        Returns (bool, message)
        """
        new_bounds = menu_item.get_bounds()
        
        # 1. Check frame boundaries
        if not contains_rect(self.get_bounds(), new_bounds):
            return False, "Out of bounds"

        # 2. Check overlaps with existing items
        for existing_item in self.items:
            if overlaps(new_bounds, existing_item.get_bounds()):
                return False, "Overlap detected"

        return True, "Valid"

    def add_item(self, menu_item):
        """
        Validates and adds a menu item to the frame. 
        Uses check_item to stay DRY (Don't Repeat Yourself).
        """
        is_valid, message = self.check_item(menu_item)
        
        if not is_valid:
            raise ValueError(f"Validation Failed: {message}")

        self.items.append(menu_item)

    def render(self) -> Image.Image:
        # Create a copy of the background to draw on top of
        canvas = self.background.copy()

        for item in self.items:
            item.render(canvas)

        return canvas.resize((self.TARGET_W, self.TARGET_H), Image.Resampling.LANCZOS)