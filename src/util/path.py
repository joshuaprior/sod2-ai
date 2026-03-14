from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

ASSETS_PATH = PROJECT_ROOT / "assets"

DATA_PATH = PROJECT_ROOT / "data"
TRAINING_DATA_PATH = DATA_PATH / "training_data" / "current"

MODELS_PATH = ASSETS_PATH / "models"
MODEL_PATH = MODELS_PATH / "sod2_menu_model.pth"

SRC_PATH = PROJECT_ROOT / "src"
