import pytest
import numpy as np
from ..scan_img import scan_img

def describe_scan_img():
    
    def it_finds_an_exact_pixel_match():
        pass

    def it_ignores_differences_in_masked_regions():
        pass

    def it_respects_the_minimum_similarity_threshold():
        pass

    def it_collapses_multiple_nearby_hits_into_one_result():
        pass

    def it_handles_multiple_instances_of_the_same_template_in_the_source_image():
        pass

    def it_scans_for_multiple_templates_at_once():
        pass

    def it_returns_an_empty_list_when_no_match_exists():
        pass

    def it_handles_matches_at_all_four_corners_of_the_screen():
        pass

    def it_handles_source_images_smaller_than_the_neighborhood_range():
        pass

    def it_returns_empty_when_template_is_larger_than_source():
        pass