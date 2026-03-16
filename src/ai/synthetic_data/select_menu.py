import random
from .menus import Menu

CHANCE_FOR_MENU_TO_RENDER = 0.5
CHANCE_FOR_MENU_TO_BE_SELECTED = 0.7

def randomize_menus(items: list[Menu], probability: float) -> list[Menu]:
    """
    Randomly selects a subset of menu items to be visible in the frame. Each item has a given probability to be included.
    """
    return [item for item in items if random.random() < probability]

def randomize_selection(items: list[Menu]) -> list[Menu]:
    """
    Randomly selects one item from the list to be selected, while ensuring all others are unselected.
    """
    if not items:
        return []

    selected_item = random.choice(items)
    for item in unselect_all(items):
        item.selected = (item == selected_item)
    
    return items

def unselect_all(items: list[Menu]) -> list[Menu]:
    """
    Ensures that no items in the list are selected.
    """
    for item in items:
        item.selected = False
    return items
    

def select_menu(selected: Menu, other_items: list[Menu]) -> list[Menu]:
    """
    Ensures the target item is selected and present, then randomly 
    adds other items from the possible list.
    """
    selected.selected = True
    return [ selected, *unselect_all(randomize_menus(other_items, CHANCE_FOR_MENU_TO_RENDER))]

def unselect_menu(unselected: Menu, other_items: list[Menu]) -> list[Menu]:
    """
    Randomly adds the unselected menu or menus from other_items. Randomly decides if one of the
    menus from other_items should be selected, and selects it if so. Otherwise, all items are
    unselected. Ensures that the unselected menu is never selected.
    """
    result = randomize_selection(randomize_menus(other_items, CHANCE_FOR_MENU_TO_RENDER))
    unselected.selected = False
    
    if random.random() < CHANCE_FOR_MENU_TO_RENDER:
        result.append(unselected)

    return result   