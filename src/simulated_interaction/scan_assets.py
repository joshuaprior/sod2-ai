from pathlib import Path
from src.util import Img, Rect

TEMPLATE_RES = (2560, 1440)

def scan_for_asset(img: Img, asset_path: Path, asset: str, threshold: float | None = None) -> list[Rect]:
    mask, templates = load_scan_asset(asset_path, asset)

    if img.size != TEMPLATE_RES:
        resize_ratio = img.width / TEMPLATE_RES[0]
        for i in [mask, *templates]:
            i.resize((int(i.width * resize_ratio), int(i.height * resize_ratio)))

    if threshold is None:
        locations = img.scan(templates, mask)
    else:
        locations = img.scan(templates, mask, threshold)
    return [Rect(*loc, *mask.size) for loc in locations]

def load_scan_asset(path: Path, asset: str) -> tuple[Img, list[Img]]:
    """
    Loads the mask and templates for a specific asset.
    
    Args:
        asset: The name of the asset (e.g., 'small_facility')
        path: The directory path containing the assets
        
    Returns:
        A tuple of (mask, templates)
    """
    
    # validate asset name
    mask_path = path / f"{asset}_mask.bmp"
    template_pattern = f"{asset}_template*.bmp"
    
    if not mask_path.exists():
        raise FileNotFoundError(f"Mask not found: {mask_path}")
    
    template_paths = sorted(list(path.glob(template_pattern)))
    if not template_paths:
        raise FileNotFoundError(f"No templates found for asset: {asset} in {path}")
    
    # load images
    mask = Img.from_file(mask_path)
    templates = [Img.from_file(img) for img in template_paths]
    
    return mask, templates