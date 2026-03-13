import importlib
from PIL import Image
from src.util.path import PROJECT_ROOT
from src.ai.synthetic_data.menus.menus import Menu

# Internal cache to store loaded icon objects
_ICON_CACHE = {}

def get_menu(menu: Menu):
    """
    Factory method that now uses an internal cache to avoid repeated disk reads.
    """
    # 1. Check if the icon is already in memory
    if menu not in _ICON_CACHE:
        full_icon_path = PROJECT_ROOT / menu.icon_path
        # Load and convert once, then store in the dictionary
        _ICON_CACHE[menu] = Image.open(full_icon_path).convert("RGBA")
        print(f"--- Cache Miss: Loaded {menu.name} from disk ---")

    # 2. Get the icon from cache
    icon_image = _ICON_CACHE[menu]

    # 3. Dynamically Load the Class
    module_path, class_name = menu.class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    menu_class = getattr(module, class_name)

    # 4. Construct
    return menu_class(icon_image=icon_image)