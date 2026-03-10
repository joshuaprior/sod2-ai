import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import shutil
from pathlib import Path

# Use your path utility and shared transforms
from util.path import DATA_PATH, MODELS_PATH
from ai.get_frame_transforms import get_frame_transforms

def run():
    print("--- Auditing Workshop Training Data ---")
    
    # 1. Setup Paths
    workshop_dir = DATA_PATH / "training_data" / "workshop"
    debug_dir = DATA_PATH / "debug_output"
    success_dir = debug_dir / "success"
    fail_dir = debug_dir / "fail"
    
    # Clean/Create debug folders
    for d in [success_dir, fail_dir]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    # 2. Load Model
    # We must match the structure used in training
    device = torch.device("cpu")
    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features, 2) # 2 classes
    
    model_path = MODELS_PATH / "sod2_menu_model.pth"
    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}")
        return
        
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # 3. Process Images
    transform = get_frame_transforms()
    # Note: We need to know the index for 'workshop'
    # Based on alpha order (not_workshop=0, workshop=1), workshop is index 1
    WORKSHOP_IDX = 1
    
    images = list(workshop_dir.glob("*.bmp"))
    print(f"Auditing {len(images)} workshop images...")

    success_count = 0
    fail_count = 0

    with torch.no_grad():
        for img_path in images:
            # Load and transform
            img = Image.open(img_path)
            input_tensor = transform(img).unsqueeze(0)
            
            # Predict
            output = model(input_tensor)
            prediction = torch.argmax(output).item()
            
            # Sort into folders
            if prediction == WORKSHOP_IDX:
                shutil.copy(img_path, success_dir / img_path.name)
                success_count += 1
            else:
                shutil.copy(img_path, fail_dir / img_path.name)
                fail_count += 1

    print(f"\nAudit Complete!")
    print(f"Successfully identified: {success_count}")
    print(f"Failed to identify: {fail_count}")
    print(f"Check results in: {debug_dir}")

if __name__ == "__main__":
    run()