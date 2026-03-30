import cv2
import numpy as np
from pathlib import Path
from .operations.scan_img import scan_img
from .operations.resize import resize

class Img:
    HOT_PINK = (255, 0, 255)
    BLACK = (0, 0, 0)

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

    def label(self, label: str, rect: tuple[int, int, int, int], color=HOT_PINK, text_color=BLACK):
        """
        Draws a 1px border around the specified rectangle (x, y, w, h).
        The border is drawn 1px outside the bounds to avoid covering content.
        Includes a text label with a solid background.
        """
        x, y, w, h = rect
        
        # Draw the Bounding Box (1px outside)
        top_left = (x - 1, y - 1)
        bottom_right = (x + w, y + h)
        cv2.rectangle(self._data, top_left, bottom_right, color, 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        thickness = 1
        padding = 4
        
        # Calculate text size (width, height), baseline
        (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)

        # Draw Text Background Rectangle, -1 thickness fills the rectangle
        bg_top_left = (x - 1, y - 1 - text_h - baseline - padding * 2)
        bg_bottom_right = (x - 1 + text_w + padding * 2, y - 1)
        cv2.rectangle(self._data, bg_top_left, bg_bottom_right, color, -1)

        # Draw the Text
        text_origin = (x - 1 + padding, y - 1 - baseline - padding)
        cv2.putText(self._data, label, text_origin, font, font_scale, text_color, thickness, cv2.LINE_AA)

    def paste(self, img: "Img", x: int, y: int):
        """
        Pastes another Img into this one at the given (x, y) coordinates.
        This is an opaque copy (no alpha blending).
        """
        w, h = img.size
        self._data[y : y + h, x : x + w] = img.raw_data

    def crop(self, x1: int, y1: int, x2: int, y2: int) -> "Img":
        """ Returns a 'view' by default (shares memory with original). """
        data = self._data[y1:y2, x1:x2]
        return Img(data)
    
    def fill(self, color: tuple[int, int, int]):
        """ Fills the entire image with the specified RGB color. """
        self._data[:] = color

    def resize(self, target_res: tuple[int, int]) -> None:
        """ Resizes the image to the target resolution. """
        self._data = resize(self._data, target_res)

    def save(self, path: Path):
        """
        Saves the image to disk. The format is determined by the 
        file extension in the path (.bmp, .png, etc.).
        """
        # Convert internal RGB to BGR before saving
        data = cv2.cvtColor(self._data, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(path), data)

    def scan(self, templates: list["Img"], mask: "Img", threshold: float|None = None) -> list[tuple[int, int]]:
        templates = [template.raw_data for template in templates]
        mask = mask.raw_data

        if threshold is None:
            return scan_img(self.raw_data, templates, mask)
        else:
            return scan_img(self.raw_data, templates, mask, threshold)

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