import win32gui

def list_window_titles():
    print(f"{'HWND':<10} | {'Window Title'}")
    print("-" * 50)
    
    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                print(f"{hwnd:<10} | '{title}'")

    win32gui.EnumWindows(enum_windows_callback, None)

if __name__ == "__main__":
    list_window_titles()