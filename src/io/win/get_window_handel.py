import win32gui # type: ignore

def get_window_handle(window_title):
    """
    Finds the HWND of a window by window title.
    """
    hwnd = win32gui.FindWindow(None, window_title)
    
    if not hwnd:
        print(f"Error: Could not find window '{window_title}'")
        return False
    
    return hwnd