from PIL import Image

def crop_frame(img: Image.Image, target_ratio=(1, 1), h_pos='center', v_pos='center'):
    """
    Crops an image to a specific aspect ratio to prevent squishing during resize.
    h_pos: 'left', 'center', 'right'
    v_pos: 'top', 'center', 'bottom'
    """
    width, height = img.size
    target_w, target_h = target_ratio
    
    img_ratio = width / height
    target_ratio_val = target_w / target_h
    
    if img_ratio > target_ratio_val:
        # Image is too wide (e.g., 21:9) -> Crop width
        new_height = height
        new_width = int(target_ratio_val * height)
    else:
        # Image is too tall -> Crop height
        new_width = width
        new_height = int(width / target_ratio_val)
        
    # Horizontal Anchor
    if h_pos == 'left':
        left = 0
    elif h_pos == 'right':
        left = width - new_width
    else: # center
        left = (width - new_width) // 2
        
    # Vertical Anchor
    if v_pos == 'top':
        top = 0
    elif v_pos == 'bottom':
        top = height - new_height
    else: # center
        top = (height - new_height) // 2
        
    return img.crop((left, top, left + new_width, top + new_height))