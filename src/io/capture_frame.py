import platform

def capture_frame():
    if platform.system() == "Windows":
        from .win.capture_frame import capture_frame
        return capture_frame()
    else:
        raise NotImplementedError