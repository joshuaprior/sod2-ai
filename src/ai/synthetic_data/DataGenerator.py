from typing import Generator
import random
from tqdm import tqdm
from src.util import Img
from src.ai import FeatureMap
from src.ai.synthetic_data import ClipCache

def slot_class_names(slots: int) -> Generator[tuple[int, str], None, None]:
    """Generates class names for the given number of slots, including an 'unselected' class."""
    classes = ["unselected"] + [f"slot_{i:02d}" for i in range(slots)]
    for index, name in enumerate(classes):
        yield index - 1, name

class DataGenerator:
    def __init__(self, slots: ClipCache):
        self.slots = slots
        self.feature_map = FeatureMap()

        self.generators = {}
        for selected_index, name in slot_class_names(FeatureMap.SLOT_CAPACITY):
            self.generators[name] = lambda i=selected_index: self._populate_slots(i)

    def _populate_slots(self, selected_slot: int):
        min_active = selected_slot if selected_slot != -1 else 1
        max_active = self.feature_map.SLOT_CAPACITY - 1
        active = random.randint(min_active, max_active)

        for i in range(active + 1):
            if i == selected_slot:
                self.feature_map.slots.add_slot(self.slots.get_selected())
            else:
                self.feature_map.slots.add_slot(self.slots.get_unselected())
    
    def generate_image(self, class_name: str, canvas: Img=None) -> Img:
        """
        Generates a single feature map image for the given class name. 
        If no canvas is provided, a new one will be created.
        """
        if canvas is None:
            canvas = Img.from_dimensions(*FeatureMap.CANVAS_RESOLUTION)

        feature_map_generator = self.generators[class_name]
        if feature_map_generator is None:
            raise ValueError(f"Invalid class name: {class_name}")
        
        self.feature_map.clear()
        feature_map_generator()
        return self.feature_map.render(canvas)
    
    @classmethod
    def generate_to_disk(cls, samples_per_class, slots: ClipCache, output_path, progress=False):
        generator = cls(slots)

        for _, name in slot_class_names(FeatureMap.SLOT_CAPACITY):
            class_dir = output_path / name
            class_dir.mkdir(parents=True, exist_ok=True)

            iterator = range(samples_per_class)
            if progress:
                iterator = tqdm(iterator, desc=f"Generating {name}")
            
            for i in iterator:
                img = generator.generate_image(name)
                img.save(class_dir / f"{name}_{i:04d}.bmp")

    @classmethod
    def create_canvas(cls) -> Img:
        return FeatureMap.create_canvas()
    