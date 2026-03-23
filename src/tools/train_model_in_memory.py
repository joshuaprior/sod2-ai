import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from tqdm import tqdm

from src.util.path import MODELS_PATH, MODEL_PATH, ASSETS_PATH
from src.ai import FeatureMap, get_frame_transforms
from src.ai.synthetic_data import DataGenerator, ClipCache
from src.ai.synthetic_data.DataGenerator import slot_class_names

# --- 1. The In-Memory Dataset ---
class SyntheticMenuDataset(Dataset):
    def __init__(self, samples_per_class: int, slots: ClipCache):
        self.generator = DataGenerator(slots)
        # We get the list of class names from our generator helper
        self.classes = [name for _, name in slot_class_names(FeatureMap.SLOT_CAPACITY)]
        self.samples_per_class = samples_per_class
        
        # Standard PyTorch normalization/tensor transforms
        self.transform = get_frame_transforms()

    def __len__(self):
        return len(self.classes) * self.samples_per_class

    def __getitem__(self, index):
        # Determine which class this index belongs to
        class_index = index % len(self.classes)
        class_name = self.classes[class_index]

        # Generate the Img object in RAM
        # This uses your new high-speed NumPy/Img renderer
        img = self.generator.generate_image(class_name)
        
        # Convert our Img.raw_data (NumPy) to a PyTorch Tensor
        # ToTensor() handles the scaling and channel swap automatically
        tensor = self.transform(img.raw_data)
        
        return tensor, class_index

def run():
    # --- 2. Setup Data Engine ---
    SLOTS_ASSETS_PATH = ASSETS_PATH / "synthetic_data" / "clips"
    tips = ClipCache.from_directory(FeatureMap.SLOT_RESOLUTION, SLOTS_ASSETS_PATH)
    
    # We'll generate 100 variations of every class per epoch
    dataset = SyntheticMenuDataset(samples_per_class=1000, slots=tips)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"--- In-Memory Training Initialized ---")
    print(f"Device: {device}")
    print(f"Total Virtual Images: {len(dataset)}")

    # --- 3. Model Architecture (ResNet-18) ---
    model = models.resnet18(weights='IMAGENET1K_V1')
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(dataset.classes))

    # Resume logic if a model exists
    if MODEL_PATH.exists():
        print(f"Loading existing brain from {MODEL_PATH}...")
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    
    model.to(device)

    # --- 4. Loss and Optimizer ---
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    # --- 5. The Training Loop ---
    TRAINING_EPOCHS = 5
    model.train()

    for epoch in range(TRAINING_EPOCHS):
        running_loss = 0.0
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{TRAINING_EPOCHS}")
        
        for inputs, labels in pbar:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        # Save progress
        MODELS_PATH.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Epoch {epoch+1} Finished. Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    run()