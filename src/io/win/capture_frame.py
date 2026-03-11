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

    # Get ONLY the client area (excludes title bar, borders, etc.)
    # left and top are always 0 here; right and bottom are width and height
    _, _, width, height = win32gui.GetClientRect(hwnd)

    if width <= 0 or height <= 0:
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
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # Flag 1 = PW_CLIENTONLY
        # Flag 2 = PW_RENDERFULLCONTENT (often required for newer Win10+ styles)
        # Combining them (3) ensures we render correctly and only target the client area
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
        
        if result == 0:
            return None

        bmp_info = save_bitmap.GetInfo()
        bmp_str = save_bitmap.GetBitmapBits(True)
        
        img = np.frombuffer(bmp_str, dtype='uint8')
        img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
        
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    finally:
        if save_bitmap:
            win32gui.DeleteObject(save_bitmap.GetHandle())
        if save_dc:
            save_dc.DeleteDC()
        if mfc_dc:
            mfc_dc.DeleteDC()
        if hwnd_dc:
            win32gui.ReleaseDC(hwnd, hwnd_dc)