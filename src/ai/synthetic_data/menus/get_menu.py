import importlib
from PIL import Image
from src.util.path import PROJECT_ROOT
from src.ai.synthetic_data.menus.menus import Menu

def get_menu(menu: Menu):
    """
    Factory method to construct a menu item class.
    Position and Selected states are now set on the instance.
    """
    # 1. Load the Icon
    full_icon_path = PROJECT_ROOT / menu.icon_path
    icon_image = Image.open(full_icon_path).convert("RGBA")

    # 2. Dynamically Load the Class
    module_path, class_name = menu.class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    menu_class = getattr(module, class_name)

    # 3. Construct with only the icon
    return menu_class(icon_image=icon_image)