import json
from src.util import Img
from src.util.path import DATA_PATH, MODEL_PATH, PROJECT_ROOT
from src.io import capture_frame
from src.ai import Model, FeatureMap

# --- Configuration ---
# Point this to a real screenshot for testing if not running live
TEST_IMAGE_PATH = DATA_PATH / "raw_screenshots" / "sod2_093559_920812.bmp"

class ClipInference:
    def __init__(self):
        # Load the model from disk; it handles its own eval() state and device
        self.model = Model.from_file(MODEL_PATH)
        self.config = self._load_config()

    def _load_config(self):
        config_path = PROJECT_ROOT / "src" / "ai" / "facilities.json"
        with open(config_path, "r") as f:
            return json.load(f)

    def stitch_frame(self, full_frame: Img, home_site_class: str) -> Img:
        """
        Extracts clips from the live frame and stitches them into 
        a 224x224 FeatureMap using the NumPy-based Img class.
        """
        res_data = self.config.get("2560x1440")
        if not res_data:
            raise ValueError("No configuration found for 2560x1440 resolution.")
            
        tip_coords = res_data["framing"]["small_facility"]["tip"]
        home_site = next((s for s in res_data["home_sites"] if s["class"] == home_site_class), None)
        
        if not home_site:
            raise ValueError(f"Home site class '{home_site_class}' not found in config.")
            
        # 1. Initialize our high-speed FeatureMap
        fm = FeatureMap()
        
        # 2. Populate slots based on game-site coordinates
        for i, slot in enumerate(home_site["slots"]):
            if i >= FeatureMap.SLOT_CAPACITY: 
                break
            
            offset_x, offset_y = slot["pos"]
            
            # Extract 15x15 region directly via NumPy slicing (Img.crop)
            clip = full_frame.crop(
                tip_coords[0] + offset_x,
                tip_coords[1] + offset_y,
                tip_coords[0] + offset_x + FeatureMap.SLOT_RESOLUTION[0],
                tip_coords[1] + offset_y + FeatureMap.SLOT_RESOLUTION[1]
            )
            fm.slots.add_slot(clip)
            
        # 3. Render returns a single 224x224 Img object
        return fm.render()

def run():
    print("--- Starting Clip Inference Test ---")
    inf = ClipInference()
    
    # 1. Capture live frame
    # capture_frame returns a NumPy array; we wrap it in our Img class
    raw_frame_data = capture_frame()
    if raw_frame_data is None:
        print("Capture failed. Is the game running?")
        return
        
    full_frame = Img(raw_frame_data)
    
    # 2. Stitch and Audit
    # We target 'lundegaard_lumber_mill' specifically from your facilities.json
    stitched = inf.stitch_frame(full_frame, "lundegaard_lumber_mill")
    
    debug_path = DATA_PATH / "clips" / "latest_inference_stitch.bmp"
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    stitched.save(debug_path)
    print(f"Stitched inference frame saved for audit at: {debug_path}")
    
    # 3. Predict using the Model's encapsulated inference logic
    result = inf.model.predict(stitched)
    print(f"\nModel Result: {result}")

if __name__ == "__main__":
    run()