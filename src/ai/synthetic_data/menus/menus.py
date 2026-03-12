from enum import Enum

class Menu(Enum):
    # Metadata: (Class Import Path, Icon File Path)
    FIGHTING_GYM = (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        "src/ai/synthetic_data/menus/icons/facility/small/fighting_gym.bmp"
    )
    SHOOTING_RANGE= (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        "src/ai/synthetic_data/menus/icons/facility/small/shooting_range.bmp"
    )
    WORKSHOP = (
        "src.ai.synthetic_data.menus.classes.small_facility.SmallFacility",
        "src/ai/synthetic_data/menus/icons/facility/small/workshop.bmp"
    )

    @property
    def class_path(self):
        return self.value[0]

    @property
    def icon_path(self):
        return self.value[1]