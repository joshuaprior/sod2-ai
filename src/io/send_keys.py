import platform
from .constants import Key

def send_keys(keys: list[tuple[Key, float]]):
    if platform.system() == "Windows":
        from .win.send_keys import send_keys
        return send_keys(keys)
    else:
        raise NotImplementedError