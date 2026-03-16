import random
from PIL import Image
from .frame import Frame
from .menus import Menu

def compose_frame(background: Image.Image, items: list[Menu]) -> Frame:
    """
    Composes a Frame by placing Menu items at random, non-overlapping positions.
    """
    frame = Frame(background)
    _, _, max_w, max_h = frame.get_bounds()

    for item in items:
        placed = False
        
        for _ in range(500):
            rx = random.randint(0, max_w - item.WIDTH)
            ry = random.randint(0, max_h - item.HEIGHT)
            
            item.position = (rx, ry)
            
            if frame.check_item(item):
                frame.add_item(item)
                placed = True
                break
        
        if not placed:
            print("Warning: Could not find a valid position for menu item.")

    return frame