from enum import Enum

class Menu(Enum):
    # Metadata: (Class Import Path, Icon File Path)
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