import win32con # type: ignore
import win32api # type: ignore
import time
from .get_window_handel import get_window_handle
from .constants import WINDOW_TITLE, KEY_CODES
from ..constants import Key


def send_key(hwnd, vk_code, delay=0.05):
    """
    Sends a key down and key up event to a specific window handle.
    
    Args:
        hwnd (int): The window handle.
        vk_code (int): The Virtual Key code (e.g., 0x25 for Left).
        delay (float): How long to 'hold' the key in seconds.
    """
    if not hwnd:
        return False

    # WM_KEYDOWN
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
    
    # Simulate hold time
    if delay > 0:
        time.sleep(delay)
    
    # WM_KEYUP
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
    return True


def send_keys(keys: list[tuple[Key, float]]):
    hwnd = get_window_handle(WINDOW_TITLE)
    
    if not hwnd:
        return False

    for key, delay in keys:
        send_key(hwnd, KEY_CODES[key], .05)
        time.sleep(delay)
    
    return True