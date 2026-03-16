import random
from .frame import Frame
from .menus import Menu

def _randomize_position(item: Menu, max_w: int, max_h: int):
    """
    Randomly assigns a position to the item within the given bounds.
    """
    item.position = (
        random.randint(0, max_w - item.WIDTH),
        random.randint(0, max_h - item.HEIGHT)
    )

def _place_item(frame: Frame, item: Menu) -> bool:
    """
    Attempts to place the item on the frame at a random,
    non-overlapping position. Returns True if successful,
    False if no valid position was found after multiple
    attempts.
    """
    _, _, max_w, max_h = frame.bounds

    for _ in range(500):
        _randomize_position(item, max_w, max_h)
        
        if frame.check_item(item):
            frame.add_item(item)
            return True
    
    return False

def compose_frame(frame: Frame, items: list[Menu]) -> Frame:
    """
    Composes a Frame by placing Menu items at random, non-overlapping positions.
    """
    for item in items:
        if not _place_item(frame, item):
            print("Warning: Could not find a valid position for menu item.")

    return frame