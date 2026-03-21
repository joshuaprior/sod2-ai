import random
import numpy as np
from PIL import Image
from tqdm import tqdm
from src.util.path import ASSETS_PATH, TRAINING_DATA_PATH
from src.util.bmp import save_bmp

from src.ai import FeatureMap
from src.ai.synthetic_data import DataGenerator, ClipCache 

# --- Configuration ---
SAMPLES_PER_CLASS = 1000
SLOTS_ASSETS_PATH = ASSETS_PATH / "synthetic_data" / "clips"

def run():
    print("--- Starting Synthetic Data Generation ---")
    tips = ClipCache.from_directory(FeatureMap.SLOT_RESOLUTION, SLOTS_ASSETS_PATH)
    DataGenerator.generate_to_disk(SAMPLES_PER_CLASS, tips, TRAINING_DATA_PATH, progress=True)  

if __name__ == "__main__":
    run()