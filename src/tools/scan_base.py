from src.util import DATA_PATH, Img
from src.simulated_interaction.base.base import Base

# --- Configuration ---
# TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "2560x1440" / "sod2_050903_887084.bmp"
# TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "1280x960"/ "sod2_140338_229694.bmp"
#TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "1280x960"/ "sod2_141215_722187.bmp"
TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "1280x960"/ "sod2_141222_460092.bmp"



def run():
    base = Base()
    next(base.scan(Img.from_file(TEST_IMAGE_PATH)))