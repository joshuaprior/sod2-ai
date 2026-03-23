import json
import torch
import numpy as np
from PIL import Image
from torchvision import models
from src.util.path import DATA_PATH, PROJECT_ROOT, MODEL_PATH
from src.ai.get_frame_transforms import get_frame_transforms
from src.io.capture_frame import capture_frame


# --- Configuration ---
# Point this to a real screenshot from your raw_screenshots directory
TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "sod2_093559_920812.bmp"
BG_COLOR = (195, 195, 195)
SLOT_DIM = 15
IMG_SIZE = 224

class ClipInference:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config = self._load_config()
        self.transform = get_frame_transforms()
        
        # New Class Names: slot_01 ... slot_22 + unselected
        self.class_names = [f"slot_{i+1:02d}" for i in range(22)] + ["unselected"]
        self.model = self._load_model()

    def _load_config(self):
        config_path = PROJECT_ROOT / "src" / "ai" / "facilities.json"
        with open(config_path, "r") as f:
            return json.load(f)

    def _load_model(self):
        # Recreate the ResNet-18 architecture with 23 output classes
        model = models.resnet18()
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Linear(num_ftrs, len(self.class_names))
        
        if MODEL_PATH.exists():
            model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
            print(f"Loaded model weights from {MODEL_PATH}")
        else:
            print("Warning: Model weights not found. Predictions will be random.")
            
        model.to(self.device)
        model.eval()
        return model

    def stitch_frame(self, full_frame: Image.Image, home_site_class: str):
        """Extracts clips from the live frame and stitches them into 224x224."""
        # Targeting the 2560x1440 resolution block in the config
        res_data = self.config.get("2560x1440")
        if not res_data:
            raise ValueError("No configuration found for 2560x1440 resolution.")
            
        tip_coords = res_data["framing"]["small_facility"]["tip"]
        
        # Find the specific home site slots
        home_site = next((s for s in res_data["home_sites"] if s["class"] == home_site_class), None)
        if not home_site:
            raise ValueError(f"Home site class '{home_site_class}' not found in config.")
            
        slots = home_site["slots"]
        
        # Create base canvas with the background gray color
        canvas = Image.new("RGB", (IMG_SIZE, IMG_SIZE), BG_COLOR)
        
        for i, slot in enumerate(slots):
            # We only support up to 22 slots based on the stitched image design
            if i >= 22: break
            
            offset_x, offset_y = slot["pos"]
            
            # Extract the 15x15 region (centered, no jiggle)
            # tip_coords are [x1, y1, x2, y2]
            crop_box = (
                tip_coords[0] + offset_x,
                tip_coords[1] + offset_y,
                tip_coords[0] + offset_x + SLOT_DIM,
                tip_coords[1] + offset_y + SLOT_DIM
            )
            
            clip = full_frame.crop(crop_box)
            
            # Determine destination based on column
            dest_x = 0 if i < 11 else 16
            dest_y = 49 + ((i % 11) * 16)
            
            canvas.paste(clip, (dest_x, dest_y))
            
        return canvas

    def predict(self, stitched_img: Image.Image):
        """Runs the stitched image through the model and returns the class name."""
        img_tensor = self.transform(stitched_img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(img_tensor)
            _, preds = torch.max(outputs, 1)
            
        return self.class_names[preds[0]]

def run():
    print("--- Starting Clip Inference Test ---")
    inf = ClipInference()
    
    if not TEST_IMAGE_PATH.exists():
        print(f"Error: Test image not found at {TEST_IMAGE_PATH}")
        return

    # Load and process the live frame
    # full_frame = Image.open(TEST_IMAGE_PATH).convert("RGB")
    full_frame = Image.fromarray(capture_frame())
    
    # 1. Stitch (Using the specified home site from your config)
    # This correctly targets Lundegaard Lumber Mill's 3 slots
    stitched = inf.stitch_frame(full_frame, "lundegaard_lumber_mill")
    
    # 2. Save for Audit
    output_dir = DATA_PATH / "clips"
    output_dir.mkdir(parents=True, exist_ok=True)
    debug_path = output_dir / "latest_inference_stitch.bmp"
    stitched.save(debug_path)
    print(f"Stitched inference frame saved for audit at: {debug_path}")
    
    # 3. Predict
    result = inf.predict(stitched)
    print(f"\nModel Result: {result}")

if __name__ == "__main__":
    run()