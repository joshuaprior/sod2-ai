import importlib
from PIL import Image
from src.util.path import PROJECT_ROOT # Assuming you have a root path util
from src.ai.synthetic_data.menus.menus import MenuType

def get_menu(menu_type: MenuType, position: tuple, selected: bool = False):
    """
    Factory method to construct a menu item class based on MenuType metadata.
    """
    # 1. Load the Icon
    # Construct absolute path using your project root and enum metadata
    full_icon_path = PROJECT_ROOT / menu_type.icon_path
    if not full_icon_path.exists():
        raise FileNotFoundError(f"Icon not found: {full_icon_path}")
    icon_image = Image.open(full_icon_path).convert("RGBA")

    # 2. Dynamically Load the Class
    # Split "module.path.ClassName" into "module.path" and "ClassName"
    module_path, class_name = menu_type.class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    menu_class = getattr(module, class_name)

    # 3. Construct and Return
    return menu_class(icon_image=icon_image, position=position, selected=selected)