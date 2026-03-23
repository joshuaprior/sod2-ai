from PIL import Image
from src.util import classproperty, Img

class SlotList:
    def __init__(self, capacity: int, resolution: tuple[int, int]):
        self._capacity = capacity
        self._resolution = resolution

        self._values = []
        
    @property
    def CAPACITY(self):
        return self._capacity

    @property
    def RESOLUTION(self):
        return self._resolution

    def _validate_dense_list(self, index: int):
        preceding_null_index = next((
            index
            for index in range(index, -1, -1)
            if self._values[index] is None
        ), None)
        return preceding_null_index is None
    
    def set_slot(self, index: int, img: Img):
        raise NotImplementedError()

    def add_slot(self, img: Img):
        if len(self._values) >= self.CAPACITY:
            raise IndexError(f"Cannot add more than {self.CAPACITY} slots.")
        
        if img.size != self.RESOLUTION:
            raise ValueError(f"Image resolution {img.size} does not match required {self.RESOLUTION}.")
        
        self._values.append(img)

    def clear(self):
        self._values.clear()

    def append(self, value: list[Img]):
        raise NotImplementedError()
    
    def items(self):
        return ((index, img) for index, img in enumerate(self._values) if img is not None)



class FeatureMap:
    def __init__(self):
        self._slots = SlotList(22, FeatureMap.SLOT_RESOLUTION)
        self._background_color = (195, 195, 195)
        self._canvas_size = FeatureMap.CANVAS_RESOLUTION

    @classproperty
    def CANVAS_RESOLUTION(cls) -> tuple[int, int]:
        return (224, 224)

    @classproperty
    def SLOT_RESOLUTION(cls) -> tuple[int, int]:
        return (15, 15)
    
    @classproperty
    def SLOT_CAPACITY(cls) -> int:
        return 22

    @property
    def slots(self):
        return self._slots

    def _get_slot_pos(self, index: int) -> tuple[int, int]:
        if 0 > index or index >= self.slots.CAPACITY:
            raise IndexError(f"Slot index {index} is out of bounds (0-{self.slots.CAPACITY - 1})")
        
        x = 0 if index < 11 else 16
        y = 49 + (index % 11) * 16
        return (x, y)
        

    def render(self, canvas: Img=None) -> Img:
        if canvas is None:
            canvas = Img.from_dimensions(*self._canvas_size)

        if canvas.size != self._canvas_size:
            raise ValueError(f"Canvas size {canvas.size} does not match required {self._canvas_size}.")
        
        canvas.fill(self._background_color)

        for index, img in self.slots.items():
            pos = self._get_slot_pos(index)
            
            # Paste img into the correct position on the canvas based on bounds
            canvas.paste(img, pos)
        
        return canvas
    
    def clear(self):
        self._slots.clear()