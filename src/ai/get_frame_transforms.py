import warnings
from torchvision import transforms

NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

def get_frame_transforms():
    """
    Builds the image transformation pipeline.
    """
    # Transforms
    tensor = transforms.ToTensor()
    normalize = transforms.Normalize(NORM_MEAN, NORM_STD)
    
    pipeline = [tensor, normalize]

    return transforms.Compose(pipeline)