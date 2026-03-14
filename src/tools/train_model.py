import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from src.util.path import DATA_PATH, MODELS_PATH
from src.ai import get_frame_transforms

# Define our directory structure
TRAINING_DATA_PATH = DATA_PATH / "training_data"
MODEL_PATH = MODELS_PATH / "sod2_menu_model.pth"

# Create models directory if it doesn't exist (like mkdir -p)
MODELS_PATH.mkdir(parents=True, exist_ok=True)

def run():
    # --- 1. Data Pre-processing ---
    # ResNet-18 expects 224x224 images and specific color normalization
    data_transforms = get_frame_transforms()

    # Load dataset: automatically maps folder names to labels (0 and 1)
    dataset = datasets.ImageFolder(str(TRAINING_DATA_PATH), transform=data_transforms)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    class_names = dataset.classes
    print(f"--- Training Initialized ---")
    print(f"Classes found: {class_names}")
    print(f"Total images: {len(dataset)}")

    # --- 2. The Model (ResNet-18) ---
    # We load a pre-trained model (it already knows how to see shapes/colors)
    model = models.resnet18(weights='IMAGENET1K_V1')
    
    
    # "Freeze" the base layers (don't rewrite the parts that recognize basic shapes)
    for param in model.parameters():
        param.requires_grad = False

    # Replace the 'head' (the final decision maker) to fit our 2 classes
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))

    # --- 3. Loss and Optimizer ---
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

    # --- 4. The Training Loop ---
    TRAINING_EPOCHS = 10
    model.train()
    print(f"Starting {TRAINING_EPOCHS} Epochs of learning...")
    
    for epoch in range(TRAINING_EPOCHS):
        running_loss = 0.0
        for inputs, labels in dataloader:
            optimizer.zero_grad()   # Reset gradients (like clearing a buffer)
            outputs = model(inputs) # Forward pass: Make a guess
            loss = criterion(outputs, labels) # Calculate how wrong we were
            loss.backward()         # Backpropagation: Find out which weights caused the error
            optimizer.step()        # Update weights: Adjust weights to reduce error
            
            running_loss += loss.item()
        
        avg_loss = running_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{TRAINING_EPOCHS} | Loss: {avg_loss:.4f}")

    # --- 5. Save the Brain ---
    # We save the 'state_dict' which is essentially the Map of learned weights
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"\nSuccess! The brain has been saved to: {MODEL_PATH}")

if __name__ == "__main__":
    run()