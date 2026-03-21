import random
from pathlib import Path
from PIL import Image

class ClipCache:
  def __init__(self, target_res: tuple[int, int], selected_clips: list[Image.Image], unselected_clips: list[Image.Image]):
    self._target_res = target_res
    self._selected_clips = selected_clips
    self._unselected_clips = unselected_clips

    w, h = target_res
    for clip in selected_clips + unselected_clips:
      if clip.width < w or clip.height < h:
        raise ValueError(f"Clip image resolution {clip.size} is not big enough to be clipped to {target_res}.")

  def _jiggle_crop(self, img: Image.Image) -> Image.Image:
    w, h = self._target_res
    x = random.randint(0, img.width - w)
    y = random.randint(0, img.height - h)
    return img.crop((x, y, x + w, y + h))

  def get_selected(self) -> Image.Image:
    return self._jiggle_crop(random.choice(self._selected_clips))
  
  def get_unselected(self) -> Image.Image:
    return self._jiggle_crop(random.choice(self._unselected_clips))
  
  @classmethod
  def from_directory(cls, target_res: tuple[int, int], path) -> "ClipCache":
      """Loads all clips from a directory into a list of PIL Images."""
      path = Path(path)
      selected_path = path / "selected"
      selected = [Image.open(f).convert("RGB") for f in selected_path.glob("*.bmp")]

      unselected_path = path / "unselected"
      unselected = [Image.open(f).convert("RGB") for f in unselected_path.glob("*.bmp")]

      return  cls(target_res, selected, unselected)