from torchvision import transforms
from .crop_frame import crop_frame

AI_IMAGE_SIZE = (224, 224)
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

def get_frame_transforms(crop_params=None):
    """
    Builds the image transformation pipeline.
    If crop_params is None, crop_frame uses its own internal defaults.
    """
    # Ensure crop_params is at least an empty dict to trigger the call
    params = crop_params if crop_params is not None else {}
    
    return transforms.Compose([
        # Always crop to prevent resolution-based squishing
        transforms.Lambda(lambda img: crop_frame(img, **params)),
        
        # Standardize to AI input size
        transforms.Resize(AI_IMAGE_SIZE),
        
        transforms.ToTensor(),
        transforms.Normalize(NORM_MEAN, NORM_STD)
    ])