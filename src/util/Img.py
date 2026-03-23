import cv2
import numpy as np
from pathlib import Path

class Img:
    def __init__(self, data: np.ndarray):
        if not isinstance(data, np.ndarray):
            raise TypeError("Img constructor requires a numpy ndarray.")
        
        self._data = data

    @property
    def raw_data(self) -> np.ndarray:
        return self._data

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)

    @property
    def width(self) -> int:
        return self._data.shape[1]

    @property
    def height(self) -> int:
        return self._data.shape[0]
    
    def paste(self, img: "Img", x: int, y: int):
        """
        Pastes another Img into this one at the given (x, y) coordinates.
        This is an opaque copy (no alpha blending).
        """
        # 1. Determine the boundaries of the source image
        w, h = img.size

        # 2. Use Slice Assignment to copy the pixels
        self._data[y : y + h, x : x + w] = img.raw_data

    def crop(self, x1: int, y1: int, x2: int, y2: int) -> "Img":
        """ Returns a 'view' by default (shares memory with original). """
        data = self._data[y1:y2, x1:x2]
        return Img(data)
    
    def fill(self, color: tuple[int, int, int]):
        """ Fills the entire image with the specified RGB color. """
        self._data[:] = color

    def save(self, path: Path):
        """
        Saves the image to disk. The format is determined by the 
        file extension in the path (.bmp, .png, etc.).
        """
        # Convert internal RGB to BGR before saving
        data = cv2.cvtColor(self._data, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(path), data)

    @classmethod
    def from_file(cls, path: Path) -> "Img":
        """
        Loads a BMP or PNG from disk into a NumPy RGB array.
        PNG alpha channels are discarded.
        """
        # cv2.imread loads BGR by default
        bgr_data = cv2.imread(str(path))
        
        if bgr_data is None:
            raise FileNotFoundError(f"Could not load image at {str(path)}")

        # Convert BGR to RGB
        data = cv2.cvtColor(bgr_data, cv2.COLOR_BGR2RGB)
        
        return cls(data)
    
    @classmethod
    def from_img(cls, img: "Img") -> "Img":
        """
        Creates a new Img by copying the pixel data from another Img.
        This is a deep copy (allocates new memory).
        """
        return cls(img.raw_data.copy())
    
    @classmethod
    def from_dimensions(cls, width: int, height: int) -> "Img":
        """ Creates a new Img with the given dimensions. """
        data = np.full((height, width, 3), (0, 0, 0), dtype=np.uint8)
        return cls(data)

    def __repr__(self):
        return f"<Img {self.width}x{self.height} at {hex(id(self))}>"