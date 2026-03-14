import cv2
import numpy as np
from PIL import Image
from torchvision import transforms

# Updated imports to use your new path utility
from util.path import DATA_PATH
from ai.get_frame_transforms import get_frame_transforms

def run():
    print("--- Resize Debugger ---")
    
    # 1. Setup Paths using your util
    workshop_dir = DATA_PATH / "training_data" / "workshop"
    output_path = DATA_PATH / "debug_resized_workshop.bmp"

    # Find the first bmp file
    images = list(workshop_dir.glob("*.bmp"))
    if not images:
        print(f"Error: No .bmp images found in {workshop_dir}")
        return

    source_img_path = images[0]
    print(f"Processing: {source_img_path.name}")

    # 2. Load the image
    img = Image.open(source_img_path).convert("RGB")
    
    # 3. Apply ONLY the Resize part of your pipeline
    # Grabbing the first transform (Resize) from your shared module
    pipeline = get_frame_transforms().transforms
    debug_pipeline = transforms.Compose([pipeline[0], pipeline[1]])

    resized_img = debug_pipeline(img)

    # 4. Save the result
    # Convert back to BGR for standard Windows .bmp compatibility
    final_output = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_path), final_output)

    print(f"Success! Resized image saved to: {output_path}")
    print(f"New dimensions: {resized_img.size}")