from PokePY.infrastructure.assets import AssetLoader

class MapMaskService:
    def __init__(self, assets: AssetLoader):
        self.assets = assets

    def is_in_grass(self, zone_name: str, x: int, y: int) -> bool:
        mask = self.assets.load_zone_mask(zone_name)
        if mask is None:
            return False
        width, height = mask.get_size()
        if not (0 <= int(x) < width and 0 <= int(y) < height):
            return False
        pixel = mask.get_at((int(x), int(y)))
        return pixel.a > 10
