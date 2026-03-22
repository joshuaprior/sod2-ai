import random
from pathlib import Path
from PIL import Image

class ClipCache:
  def __init__(self, target_res: tuple[int, int], selected_clips: list[Image.Image], unselected_clips: list[Image.Image]):
    self._target_res = target_res
    self._selected_clips = selected_clips
    self._unselected_clips = unselected_clips
    self._selected_crop_cache = [None] * len(selected_clips)
    self._unselected_crop_cache = [None] * len(unselected_clips)

    w, h = target_res
    for clip in selected_clips + unselected_clips:
      if clip.width < w or clip.height < h:
        raise ValueError(f"Clip image resolution {clip.size} is not big enough to be clipped to {target_res}.")

  def _jiggle(self, img: Image.Image) -> Image.Image:
    max_jiggle_x = img.width - self._target_res[0]
    max_jiggle_y = img.height - self._target_res[1]
    x = random.randint(0, max_jiggle_x)
    y = random.randint(0, max_jiggle_y)
    return (x, y, max_jiggle_x, max_jiggle_y)

  def _crop(self, img: Image.Image, x: int, y: int) -> Image.Image:
    w, h = self._target_res
    return img.crop((x, y, x + w, y + h))
  
  def _create_cache_matrix(self, rows, cols) -> list[list[None]]:
    return [[None] * cols for _ in range(rows)]
  
  def _get_random_clip(self, images: list[Image.Image], cache: list[list[list[Image.Image | None]]]) -> Image.Image:
    i = random.randrange(len(images))
    x, y, max_jiggle_x, max_jiggle_y = self._jiggle(images[i])

    if cache[i] is None:
      cache[i] = self._create_cache_matrix(max_jiggle_x + 1, max_jiggle_y + 1)

    if cache[i][x][y] is None:
      cache[i][x][y] = self._crop(images[i], x, y)

    return cache[i][x][y]

  def get_selected(self) -> Image.Image:
    return self._get_random_clip(self._selected_clips, self._selected_crop_cache)

  def get_unselected(self) -> Image.Image:
    return self._get_random_clip(self._unselected_clips, self._unselected_crop_cache)
  
  @classmethod
  def from_directory(cls, target_res: tuple[int, int], path) -> "ClipCache":
      """Loads all clips from a directory into a list of PIL Images."""
      path = Path(path)
      selected_path = path / "selected"
      selected = [Image.open(f).convert("RGB") for f in selected_path.glob("*.bmp")]

      unselected_path = path / "unselected"
      unselected = [Image.open(f).convert("RGB") for f in unselected_path.glob("*.bmp")]

      return  cls(target_res, selected, unselected)