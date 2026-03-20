import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models
from torch.utils.data import DataLoader
from tqdm import tqdm
from src.util.path import MODELS_PATH, MODEL_PATH, TRAINING_DATA_PATH
from src.ai import get_frame_transforms

DEBUG_MODE = False

# Create models directory if it doesn't exist
MODELS_PATH.mkdir(parents=True, exist_ok=True)

def run():
    # --- 1. Data Pre-processing ---
    if DEBUG_MODE:
        data_transforms = get_frame_transforms()
    else:
        # Optimization: Clips are already 15x15, so skip heavy processing
        data_transforms = get_frame_transforms(None, process_image=False, to_tensor=True)

    dataset = datasets.ImageFolder(str(TRAINING_DATA_PATH), transform=data_transforms)
    # Increased batch size for faster processing of small images
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    class_names = dataset.classes
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"--- Training Initialized ---")
    print(f"Device: {device}")
    print(f"Classes found: {class_names}")
    print(f"Total images: {len(dataset)}")

    # --- 2. The Model (ResNet-18) ---
    model = models.resnet18(weights='IMAGENET1K_V1')

    # "Freeze" the base layers (don't rewrite the parts that recognize basic shapes)
    # for param in model.parameters():
    #     param.requires_grad = False
    
    # Replace the 'head' to fit our 23 classes
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))

    # --- RESUME LOGIC ---
    if MODEL_PATH.exists():
        print(f"Loading existing brain from {MODEL_PATH}...")
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        
        # Unfreeze all layers for fine-tuning since we have a base to work from
        for param in model.parameters():
            param.requires_grad = True
        print("Model unfrozen for fine-tuning.")
    else:
        # Freeze base layers for the very first run to protect ImageNet features
        for param in model.parameters():
            param.requires_grad = False
        for param in model.fc.parameters():
            param.requires_grad = True
        print("Starting fresh: Base layers frozen.")

    model.to(device)

    # --- 3. Loss and Optimizer ---
    criterion = nn.CrossEntropyLoss()
    # Use a smaller learning rate if fine-tuning an existing model
    lr = 0.0001 if MODEL_PATH.exists() else 0.001
    optimizer = optim.Adam(model.parameters() if MODEL_PATH.exists() else model.fc.parameters(), lr=lr)

    # --- 4. The Training Loop ---
    TRAINING_EPOCHS = 10
    model.train()
    print(f"Starting {TRAINING_EPOCHS} Epochs of learning...")
    
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
        
        avg_loss = running_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{TRAINING_EPOCHS} Finished | Avg Loss: {avg_loss:.4f}")

        # --- SAVE AFTER EVERY EPOCH ---
        # Moving this inside the loop ensures progress is kept if the script is stopped
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Checkpoint saved: {MODEL_PATH}")

if __name__ == "__main__":
    run()