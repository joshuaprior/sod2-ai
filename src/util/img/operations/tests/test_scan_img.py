import pytest
import numpy as np
from src.util import Img

def describe_scan_img():
    
    def it_finds_an_exact_pixel_match():
        # Source: 20x20, black
        source_data = np.zeros((20, 20, 3), dtype=np.uint8)
        
        # Template: 5x5, white
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)

        # Mask: 5x5, white
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        # Paste template at (x=10, y=5)
        source_data[5:10, 10:15] = template_data
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        results = source_img.scan([template_img], mask_img, threshold=0.99)
        assert len(results) == 1
        assert results[0] == (10, 5)

    def it_ignores_differences_in_masked_regions():
        # Source: 10x10, grey
        source_data = np.full((10, 10, 3), 100, dtype=np.uint8)
        
        # Template: 5x5, grey ...EXCEPT for the center
        # pixel (2,2), which we make bright white
        template_data = np.full((5, 5, 3), 100, dtype=np.uint8)
        template_data[2, 2] = [255, 255, 255]

        # Unmask Pixel: 5x5, white
        unmasked_pixel_data = np.full((5, 5, 3), 255, dtype=np.uint8)

        # Masked Pixel: 5x5, white ...EXCEPT for the center
        # pixel (2,2), which we make black (0)
        masked_pixel_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        masked_pixel_data[2, 2] = [0, 0, 0]

        

        source_img = Img(source_data)
        template_img = Img(template_data)
        unmasked_pixel_img = Img(unmasked_pixel_data)
        masked_pixel_img = Img(masked_pixel_data)

        # Execute 1: We expect the unmasked pixel to cause no matches.
        results_unmasked_pixel = source_img.scan([template_img], unmasked_pixel_img, threshold=0.99)
                
        # Execute 2: With the pixel masked out, we should get one match.
        results_masked_pixel = source_img.scan([template_img], masked_pixel_img, threshold=0.99)

        assert len(results_unmasked_pixel) == 0
        assert len(results_masked_pixel) == 1

    def it_respects_the_minimum_similarity_threshold():
        # Source: 10x10, black, with square 5x5, dark grey
        source_data = np.zeros((10, 10, 3), dtype=np.uint8)
        source_data[2:7, 2:7] = np.full((5, 5, 3), 100, dtype=np.uint8)
        
        # Template: 3x3 black, with 1px white boarder
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        template_data[1:4, 1:4] = np.full((3, 3, 3), 0, dtype=np.uint8)

        # Mask: 5x5, white
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute 1: Very strict threshold, no matches expected 
        results_strict = source_img.scan([template_img], mask_img, threshold=0.99)
        
        # Execute 2: Loose threshold, should get one match
        results_loose = source_img.scan([template_img], mask_img, threshold=0.7)

        # Assert
        assert len(results_strict) == 0
        assert len(results_loose) == 1
        assert results_loose[0] == (2, 2)

    def it_collapses_multiple_nearby_hits_into_one_result():
        # Source: 30x30, black, with 5x5 white square
        source_data = np.zeros((30, 30, 3), dtype=np.uint8)
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        source_data[10:15, 10:15] = template_data
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(np.full((5, 5, 3), 255, dtype=np.uint8))
        
        # Execute: Using a very low threshold (0.1). 
        # Without deduplication, this would return dozens of points.
        results = source_img.scan([template_img], mask_img, threshold=0.1)
        
        # Assert: We only want the single best match point
        assert len(results) == 1
        assert results[0] == (10, 10)

    def it_handles_multiple_instances_of_the_same_template_in_the_source_image():
        # Source: 100x100, black
        source_data = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Template: 5x5, white
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)

        # Mask: 5x5, white
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        # Place two identical templates far apart
        # Match A at (10, 10)
        source_data[10:15, 10:15] = template_data
        # Match B at (50, 50)
        source_data[50:55, 50:55] = template_data
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute
        results = source_img.scan([template_img], mask_img, threshold=0.9)
        
        # Assert: We expect exactly two distinct matches
        assert len(results) == 2
        assert (10, 10) in results
        assert (50, 50) in results

    def it_scans_for_multiple_templates_at_once():
        # Source: 50x50, black
        source_data = np.zeros((50, 50, 3), dtype=np.uint8)
        
        # Template 1: 5x5, White
        t1_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        # Template 2: 5x5 Orange
        t2_data = np.full((5, 5, 3), (255, 165, 0), dtype=np.uint8)

        # Mask: 5x5, white
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        # Paste them at distinct locations
        source_data[10:15, 10:15] = t1_data # White at 10,10
        source_data[30:35, 30:35] = t2_data # Orange at 30,30
        
        source_img = Img(source_data)
        t1_img = Img(t1_data)
        t2_img = Img(t2_data)
        mask_img = Img(mask_data)
        
        # Verify Template 1 only finds the white square
        res1 = source_img.scan([t1_img], mask_img, threshold=0.9)
        assert len(res1) == 1, "Template 1 should only match the white square"
        assert (10, 10) in res1
        
        # Verify Template 2 only finds the orange square
        res2 = source_img.scan([t2_img], mask_img, threshold=0.9)
        assert len(res2) == 1, "Template 2 should only match the orange square"
        assert (30, 30) in res2

        # Execute: Now scan for both. If this returns 2, we know it's 1 per template.
        results = source_img.scan([t1_img, t2_img], mask_img, threshold=0.9)
        
        assert len(results) == 2
        assert (10, 10) in results
        assert (30, 30) in results

    def it_returns_an_empty_list_when_no_match_exists():
        # Source: 20x20, black
        source_data = np.zeros((20, 20, 3), dtype=np.uint8)
        
        # Template: 5x5, white
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)

        #mask: 5x5, white 
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute: Scan for a template that isn't in the source
        results = source_img.scan([template_img], mask_img, threshold=0.9)
        
        # Assert
        assert isinstance(results, list)
        assert len(results) == 0

    def it_handles_matches_at_all_four_corners_of_the_screen():
        # Source: 30x30, black
        source_data = np.zeros((30, 30, 3), dtype=np.uint8)
        
        # Template: 5x5, white
        template_data = np.full((5, 5, 3), 255, dtype=np.uint8)

        # Mask: 5x5, white
        mask_data = np.full((5, 5, 3), 255, dtype=np.uint8)
        
        # Paste template at all four extreme corners
        # Top Left (0,0)
        source_data[0:5, 0:5] = template_data
        # Top Right (25,0)
        source_data[0:5, 25:30] = template_data
        # Bottom Left (0,25)
        source_data[25:30, 0:5] = template_data
        # Bottom Right (25,25)
        source_data[25:30, 25:30] = template_data
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute
        results = source_img.scan([template_img], mask_img, threshold=0.99)
        
        # Assert: We expect exactly 4 matches
        assert len(results) == 4
        assert (0, 0) in results
        assert (25, 0) in results
        assert (0, 25) in results
        assert (25, 25) in results

    def it_handles_source_images_smaller_than_the_neighborhood_range():
        # Source: 6x6, black
        source_data = np.zeros((6, 6, 3), dtype=np.uint8)

        # Template: 3x3, white
        template_data = np.full((3, 3, 3), 255, dtype=np.uint8)

        # Mask: 3x3, white
        mask_data = np.full((3, 3, 3), 255, dtype=np.uint8)
        
        # Place at (1, 1)
        source_data[1:4, 1:4] = template_data
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute: This verifies the boundary checks in the neighborhood generator
        results = source_img.scan([template_img], mask_img, threshold=0.99)
        
        # Assert
        assert len(results) == 1
        assert results[0] == (1, 1)

    def it_returns_empty_when_template_is_larger_than_source():
        # Source: 5x5, black
        source_data = np.zeros((5, 5, 3), dtype=np.uint8)

        # Template: 10x10, white
        template_data = np.full((10, 10, 3), 255, dtype=np.uint8)

        # Mask: 10x10, white
        mask_data = np.full((10, 10, 3), 255, dtype=np.uint8)
        
        source_img = Img(source_data)
        template_img = Img(template_data)
        mask_img = Img(mask_data)
        
        # Execute: We expect an empty list, not a crash
        results = source_img.scan([template_img], mask_img, threshold=0.9)
        
        # Assert
        assert results == []