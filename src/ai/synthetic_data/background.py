import random
from PIL import Image
from src.util.path import ASSETS_PATH

class Background:
    """
    Manages the loading and caching of prerendered noisy backgrounds. The
    backgrounds are meant to help the model ignore pixels that are not
    related to the menus in training data.
    Ensures data integrity by validating resolution and file existence.
    """
    TARGET_RES = (2560, 1440)

    def __init__(self):
        self.bg_dir = ASSETS_PATH / "synthetic_data" / "backgrounds"
        self.bg_files = list(self.bg_dir.glob("*.bmp"))
        
        if not self.bg_files:
            raise FileNotFoundError(f"No background assets found in {self.bg_dir}. ")
            
        self._cache = {}

    def get_background(self) -> Image.Image:
        """
        Selects a random background and lazy-loads it.
        Validates that the image matches the target resolution exactly.
        """
        bg_path = random.choice(self.bg_files)
        file_key = bg_path.name

        if file_key not in self._cache:
            img = Image.open(bg_path).convert("RGB")
            
            # Strict Resolution Check
            if img.size != self.TARGET_RES:
                raise ValueError(
                    f"Background {file_key} has resolution {img.size}, "
                    f"but {self.TARGET_RES} is required. Please check your source assets."
                )
                
            self._cache[file_key] = img
            print(f"--- Background Cache: Loaded {file_key} ---")

        # Returns a copy so the cached version remains 'clean' for the next frame
        return self._cache[file_key].copy()