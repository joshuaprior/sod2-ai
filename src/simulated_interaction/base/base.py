from typing import Generator
from src.util import Img, ASSETS_PATH, DATA_PATH
from ..scan_assets import scan_for_asset
from .SmallFacility import SmallFacility
from .LargeFacility import LargeFacility

BASE_ASSETS = ASSETS_PATH / "scanning_templates" / "base"

class Base:
  def scan(self, img: Img) -> Generator[tuple[str, list[tuple[int, int]]], Img, None]:
    # left nav
    resources = scan_for_asset(img, BASE_ASSETS, "resources")
    community = scan_for_asset(img, BASE_ASSETS, "community")
    morale = scan_for_asset(img, BASE_ASSETS, "morale")
    effects = scan_for_asset(img, BASE_ASSETS, "effects")
    noise_level = scan_for_asset(img, BASE_ASSETS, "noise_level")
    siege_threat = scan_for_asset(img, BASE_ASSETS, "siege_threat")

    # facilities
    small_facilities = [
      SmallFacility("", rect)
      for rect in scan_for_asset(img, BASE_ASSETS, "small_facility")
    ]

    large_facilities = [
      LargeFacility("", rect)
      for rect in scan_for_asset(img, BASE_ASSETS, "large_facility")
    ]

    # outposts
    outposts = scan_for_asset(img, BASE_ASSETS, "outpost")

    left_nav = [*resources, *community, *morale, *effects, *noise_level, *siege_threat]

    for rect in left_nav:
      img.label("Left Nav", rect.rect)

    for facility in small_facilities:
      #img.label("Small Facility", facility.rect.rect)
      img.label("sel", facility.selection.rect, color=(255, 165, 0))
      img.label("icon", facility.icon.rect, color=(173, 216, 230))

    for facility in large_facilities:
      #img.label("Large Facility", facility.rect.rect)
      img.label("sel", facility.selection.rect, color=(255, 165, 0))
      img.label("icon", facility.icon.rect, color=(173, 216, 230))

    for rect in outposts:
      img.label("Outpost", rect.rect)
    
    img.save(DATA_PATH / "debug" / "base_scan_output.bmp")

    yield None