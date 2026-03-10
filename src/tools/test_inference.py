import torch
import torch.nn as nn
from torchvision import models, transforms
import time

from src.util import MODELS_PATH
from src.io.capture_frame import capture_frame
from src.ai import get_frame_transforms

# --- Configuration ---
MODEL_PATH = MODELS_PATH / "sod2_menu_model.pth"
CLASS_NAMES = ['not_workshop', 'workshop'] # Must match your training folder order!

# 1. Prepare the "Brain" Structure
# We must build the same ResNet-18 skeleton we used during training
model = models.resnet18()
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(CLASS_NAMES))

# 2. Inject the "Learned Weights"
# map_location='cpu' ensures it works even if you don't have a high-end GPU
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval() # Set to 'evaluation' mode (turns off dropout/batchnorm)

# 3. Define the "Preprocessing" Pipeline
# This must match EXACTLY what we used in the training script
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    *get_frame_transforms().transforms # Spreads the existing shared transforms
])

def run():
    print(f"--- Inference Test Started ---")
    print("Watching for Workshop... Press Ctrl+C to stop.")
    
    try:
        while True:
            frame = capture_frame()
            
            if frame is not None:
                # Prepare image for AI
                input_tensor = preprocess(frame)
                input_batch = input_tensor.unsqueeze(0) # Add a 'batch' dimension (1, 3, 224, 224)

                with torch.no_grad(): # Disable gradient math for faster speed
                    output = model(input_batch)
                    
                    # Convert raw scores (logits) into probabilities (0.0 to 1.0)
                    probabilities = torch.nn.functional.softmax(output[0], dim=0)
                    
                    # Get the index of the highest probability
                    confidence, index = torch.max(probabilities, 0)
                    label = CLASS_NAMES[index]
                    
                # Display result (clear terminal and print)
                percent = confidence.item() * 100
                status = f"[{label.upper()}] - Confidence: {percent:.2f}%"
                print(f"\r{status}", end="", flush=True)
                
            else:
                print("\rCapture failed. Is the game open?", end="")
            
            time.sleep(0.5) # Don't melt the CPU during testing
            
    except KeyboardInterrupt:
        print("\nTest stopped.")

if __name__ == "__main__":
    run()