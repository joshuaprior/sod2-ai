import win32gui # type: ignore
import win32ui # type: ignore
import ctypes
import numpy as np
import cv2
from .constants import WINDOW_TITLE
from .get_window_handel import get_window_handle

def capture_frame():
    hwnd = get_window_handle(WINDOW_TITLE)

    if not hwnd:
        return None

    # Get dimensions
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    if w <= 0 or h <= 0:
        return None

    hwnd_dc = None
    mfc_dc = None
    save_dc = None
    save_bitmap = None

    try:
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bitmap)

        # Use ctypes for PrintWindow to avoid library attribute errors
        # Flag 2 = PW_RENDERFULLCONTENT
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)
        if result == 0:
            result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)

        if result == 0:
            return None

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        
        img = np.frombuffer(bmp_str, dtype='uint8')
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
        
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    finally:
        if save_bitmap:
            win32gui.DeleteObject(save_bitmap.GetHandle())
        if save_dc:
            save_dc.DeleteDC()
        if mfc_dc:
            mfc_dc.DeleteDC()
        if hwnd_dc:
            win32gui.ReleaseDC(hwnd, hwnd_dc)