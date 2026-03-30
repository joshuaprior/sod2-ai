from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

"""
Assets are stored externally so the main repo remains small enough
to import into Gemini for code assit. Use external_assets() to map
a path to the external assets directory.
"""
def external_assets(path: Path) -> Path:
    ASSETS_ROOT = PROJECT_ROOT.parent / "sod2-ai-assets"

    # Ensure we are working with an absolute path
    absolute_path = path.resolve()
    
    # Calculate path relative to the PROJECT_ROOT
    try:
        relative_path = absolute_path.relative_to(PROJECT_ROOT)
    except ValueError:
        # If the path isn't inside PROJECT_ROOT, we can't mirror it correctly
        raise ValueError(f"Path {path} is not within the PROJECT_ROOT {PROJECT_ROOT}")

    return ASSETS_ROOT / relative_path

SRC_PATH = PROJECT_ROOT / "src"

DATA_PATH = PROJECT_ROOT / "data"
TRAINING_DATA_PATH = DATA_PATH / "training_data" / "current"

# External assets
MODELS_PATH = external_assets(PROJECT_ROOT / "models")
MODEL_PATH = MODELS_PATH / "sod2_menu_model.pth"


