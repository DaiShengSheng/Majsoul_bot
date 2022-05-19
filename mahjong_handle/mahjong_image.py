from collections import defaultdict
from enum import Enum

from PIL import Image

from .imghandler import cut_sprites
from .utils import get_path

__all__ = ["MahjongImage", "TilebackType"]

TilebackMap = [
    "7s",
    "6p",
    "5m",
    "9m",
    "0p",
    "0s",
    "1m",
    "1p",
    "5p",
    "6s",
    "7z",
    "9p",
    "1s",
    "2s",
    "0m",
    "3m",
    "5s",
    "6z",
    "8m",
    "9s",
    "1z",
    "3p",
    "4m",
    "4p",
    "5z",
    "7m",
    "8p",
    "back",
    "2m",
    "3s",
    "4s",
    "no_image",
    "6m",
    "7p",
    "8s",
    "2z",
    "2p",
    "3z",
    "4z",
    "no_image2",
]


class TilebackType(Enum):
    blue = "correct.png"
    orange = "exist.png"
    no_color = "no.png"


MahjongImageObj = defaultdict(dict)

for filename in TilebackType:
    img = Image.open(get_path("assets", filename.value))
    MahjongImageObj[filename] = dict(
        zip(
            TilebackMap,
            cut_sprites(
                img,
                (80, 130),
                width_padding=1,
                sprite_call=lambda img: img.convert("RGBA"),
            ),
        )
    )
    img.close()


class MahjongImage:
    __slots__ = ["type"]

    def __init__(self, type: TilebackType):
        self.type = type

    def tile(self, name):
        if name not in TilebackMap:
            return TilebackMap[self.type]["back"]
        else:
            return MahjongImageObj[self.type][name]
