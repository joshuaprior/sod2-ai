import cv2
import numpy as np
from typing import Generator

NEIGHBORHOOD_THRESHOLD = 10

def scan_img(img: np.ndarray, templates: list[np.ndarray], mask: np.ndarray, threshold: float=0.95) -> list[tuple[int, int]]:
    """
    Scans the given image for matches to the provided templates using the specified mask and threshold.
    
    Args:
        img (np.ndarray): The source image to scan.
        templates (list[np.ndarray]): A list of template images to match against.
        mask (np.ndarray): A mask image to apply during matching.
        threshold (float): The minimum correlation value to consider a match valid.
    
    Returns:
        list[tuple[int, int]]: A list of (x, y) coordinates where matches were found.
    """
    locations = []
    visited_points = set()

    for template in templates:
        if template.shape[0] > img.shape[0] or template.shape[1] > img.shape[1]:
            # template is larger than the image, no matches possible
            continue

        similarity_map = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED, mask=mask)
        # Replace any NaN or infinite values in the similarity map with 0.0 to avoid issues during thresholding
        similarity_map[~np.isfinite(similarity_map)] = 0.0
        points_y, points_x = np.where(similarity_map >= threshold)
        
        # Sort points by similarity score in descending
        # order to prioritize stronger matches
        similarities = similarity_map[points_y, points_x]
        sorted_indices = np.argsort(similarities)[::-1]
        points_sorted_by_similarity = [(points_x[index], points_y[index]) for index in sorted_indices]

        for point in points_sorted_by_similarity:
            if point in visited_points:
                continue
            
            # Visit the neighborhood of points around this point
            # to find the one with the highest similarity score
            max_similarity = -1.0
            max_similarity_point = None

            for pt in neighborhood(point, similarity_map.shape):
                similarity = similarity_map[pt[1], pt[0]]
                if similarity >= threshold:
                  visited_points.add(pt)
                  if similarity >= max_similarity:
                    max_similarity = similarity
                    max_similarity_point = pt

            locations.append(max_similarity_point)

    return locations

def neighborhood(point: tuple[int, int], shape: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
  """
  Generates points in the neighborhood of the given point within the specified proximity threshold.
  Ensures that generated points are within the bounds of the image shape.
  """
  min_x = point[0] - NEIGHBORHOOD_THRESHOLD
  max_x = point[0] + NEIGHBORHOOD_THRESHOLD
  min_y = point[1] - NEIGHBORHOOD_THRESHOLD
  max_y = point[1] + NEIGHBORHOOD_THRESHOLD

  for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
      if 0 <= x < shape[1] and 0 <= y < shape[0]:
        yield (x, y)
