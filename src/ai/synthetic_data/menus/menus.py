from enum import Enum
from src.util.path import ASSETS_PATH

ICONS_PATH = ASSETS_PATH / "synthetic_data" / "menus" / "icons"
SMALL_FACILITY_PATH = ICONS_PATH / "facility" / "small"



class Menu(Enum):
    # Metadata: (Class Import Path, Icon File Path)
    FIGHTING_GYM = (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        SMALL_FACILITY_PATH / "fighting_gym.bmp"
    )
    SHOOTING_RANGE= (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        SMALL_FACILITY_PATH / "shooting_range.bmp"
    )
    WORKSHOP = (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        SMALL_FACILITY_PATH / "workshop.bmp"
    )

    @property
    def class_path(self):
        return self.value[0]

    @property
    def icon_path(self):
        return self.value[1]