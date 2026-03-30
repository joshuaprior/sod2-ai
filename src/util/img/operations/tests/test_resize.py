import pytest
import numpy as np
from src.util import Img

def describe_resize():

    def it_returns_a_copy_when_resolutions_match():
        # Source: 10x10, gray
        data = np.full((10, 10, 3), 128, dtype=np.uint8)
        img = Img(data)
        
        # Capture the memory address of the original array
        original_data_id = id(img.raw_data)
        
        # Execute: Resize to the exact same dimensions
        img.resize((10, 10))
        
        # Assert: Values should be identical, but it must be a different object
        assert img.width == 10
        assert img.height == 10
        assert np.array_equal(img.raw_data, data)
        assert id(img.raw_data) != original_data_id

    def it_downscales_an_image():
        # Source: 20x20, gray
        data = np.full((20, 20, 3), 100, dtype=np.uint8)
        img = Img(data)
        
        # Execute
        img.resize((10, 10))
        
        # Assert
        assert img.width == 10
        assert img.height == 10
        assert img.raw_data.shape == (10, 10, 3)

    def it_upscales_an_image():
        # Source: 2x2, checkerboard (Black and White)
        data = np.zeros((2, 2, 3), dtype=np.uint8)
        data[0, 0] = [255, 255, 255]
        data[1, 1] = [255, 255, 255]
        img = Img(data)
        
        # Execute
        img.resize((10, 10))
        
        # Assert
        assert img.width == 10
        assert img.height == 10
        
        # Check the corner colors to ensure the pattern is preserved
        assert np.array_equal(img.raw_data[0, 0], [255, 255, 255])
        assert np.array_equal(img.raw_data[9, 9], [255, 255, 255])
        assert np.array_equal(img.raw_data[9, 0], [0, 0, 0])
        assert np.array_equal(img.raw_data[0, 9], [0, 0, 0])

    def it_handles_non_uniform_scaling():
        # Source: 10x10, gray
        data = np.full((10, 10, 3), 128, dtype=np.uint8)
        img = Img(data)
        
        # Execute: Scale to a rectangle (20 width, 5 height)
        img.resize((20, 5))
        
        # Assert
        assert img.width == 20
        assert img.height == 5
        assert img.raw_data.shape == (5, 20, 3)

    def it_handles_scaling_extremely_small_images():
        # Source: Single white pixel
        data = np.full((1, 1, 3), 255, dtype=np.uint8)
        img = Img(data)
        
        # Execute: Scale up to 10x10
        img.resize((10, 10))
        
        # Assert
        assert img.width == 10
        assert img.height == 10
        # Every pixel in the new image should be white
        assert np.all(img.raw_data == 255)

    def it_preserves_uint8_datatype():
        # Source: 10x10, gray
        data = np.full((10, 10, 3), 128, dtype=np.uint8)
        img = Img(data)
        
        # Execute: Resize
        img.resize((5, 5))
        
        # Assert
        assert img.raw_data.dtype == np.uint8