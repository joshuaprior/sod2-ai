from torchvision import transforms
from .crop_frame import crop_frame

AI_IMAGE_SIZE = (224, 224)
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

def get_frame_transforms(crop_params=None, process_image=True, to_tensor=True,):
    """
    Builds the image transformation pipeline.
    If crop_params is None, crop_frame uses its own internal defaults.
    """
    # Ensure crop_params is at least an empty dict to trigger the call
    params = crop_params if crop_params is not None else {}

    # Transforms
    crop = transforms.Lambda(lambda img: crop_frame(img, **params)) # Always crop to prevent resolution-based squishing
    resize = transforms.Resize(AI_IMAGE_SIZE) # Standardize to AI input size
    tensor = transforms.ToTensor()
    normalize = transforms.Normalize(NORM_MEAN, NORM_STD)
    
    pipeline = []

    if process_image:
        pipeline = [crop, resize]

    if to_tensor:
        pipeline = pipeline + [tensor, normalize]

    return transforms.Compose(pipeline)