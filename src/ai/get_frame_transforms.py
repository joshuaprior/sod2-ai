from torchvision import transforms

AI_IMAGE_SIZE = (224, 224)
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

def get_frame_transforms():
    return transforms.Compose([
        # 1. Grab a square from the middle of the 1080p frame first
        # This prevents the 'squash' effect.
        # transforms.CenterCrop(720), 
        
        # 2. Now resize that clean square to the AI's required size
        transforms.Resize(AI_IMAGE_SIZE),
        
        transforms.ToTensor(),
        transforms.Normalize(NORM_MEAN, NORM_STD)
    ])