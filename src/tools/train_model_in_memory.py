import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from tqdm import tqdm

from src.util.path import MODELS_PATH, MODEL_PATH, ASSETS_PATH
from src.ai import Model, FeatureMap
from src.ai.synthetic_data import DataGenerator, ClipCache
from src.ai.synthetic_data.DataGenerator import slot_class_names

FINE_TUNING = False

if not FINE_TUNING:
    TRAINING_EPOCHS = 10
    SAMPLES_PER_CLASS = 100
else:
    TRAINING_EPOCHS = 2
    SAMPLES_PER_CLASS = 100

SLOTS_ASSETS_PATH = ASSETS_PATH / "synthetic_data" / "clips"

def custom_collate(batch):
    imgs = [item[0] for item in batch]
    labels = torch.tensor([item[1] for item in batch])
    return imgs, labels

# --- 1. The In-Memory Dataset ---
class SyntheticMenuDataset(Dataset):
    def __init__(self, samples_per_class: int, slots: ClipCache):
        self.generator = DataGenerator(slots)
        # We get the list of class names from our generator helper
        self.classes = [name for _, name in slot_class_names(FeatureMap.SLOT_CAPACITY)]
        self.samples_per_class = samples_per_class

    def __len__(self):
        return len(self.classes) * self.samples_per_class

    def __getitem__(self, index):
        # Determine which class this index belongs to
        class_index = index % len(self.classes)
        class_name = self.classes[class_index]

        # Generate the Img object in RAM
        # This uses your new high-speed NumPy/Img renderer
        img = self.generator.generate_image(class_name)

        return img, class_index

def run():
    # --- 2. Setup Data Engine ---
    SLOTS_ASSETS_PATH = ASSETS_PATH / "synthetic_data" / "clips"
    tips = ClipCache.from_directory(FeatureMap.SLOT_RESOLUTION, SLOTS_ASSETS_PATH)
    
    # We'll generate 100 variations of every class per epoch
    dataset = SyntheticMenuDataset(samples_per_class=SAMPLES_PER_CLASS, slots=tips)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=custom_collate)

    if MODEL_PATH.exists():
        print(f"Loading existing state from {MODEL_PATH}...")
        model = Model.from_file(MODEL_PATH, training=True, fine_tuning=FINE_TUNING)
    else:
        model = Model(training=True, fine_tuning=FINE_TUNING)

    print(f"--- In-Memory Training Initialized ---")
    print(f"Device: {model.DEVICE}")
    print(f"Total Virtual Images: {len(dataset)}")

    if model.FINE_TUNING:
        print("Fine-tuning enabled: Unfreezing all layers.")
    else:
        print("Fine-tuning disabled: Freezing base layers.")

    for epoch in range(TRAINING_EPOCHS):
        running_loss = 0.0
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{TRAINING_EPOCHS}")
        
        for imgs, labels in pbar:
            loss = model.train(imgs, labels)
            running_loss += loss
            pbar.set_postfix({'loss': f'{loss:.4f}'})
        
        # Save progress
        MODELS_PATH.mkdir(parents=True, exist_ok=True)
        model.save(MODEL_PATH)
        print(f"Epoch {epoch+1} Finished. Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    run()