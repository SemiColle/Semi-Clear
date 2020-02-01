import arcade
from .Drawable import ThickLine, SpriteDrawable
from . import helper, AssetPath


class TestArena():
    def __init__(self, spriteList):
        self.drawable = ThickLine((-1, 0), (1, 0), 2, arcade.color.CAMEL, 0)
        spriteList.append(self.drawable)


class Eden3SArena():
    def __init__(self, spriteList):
        self.drawable = SpriteDrawable(AssetPath.ARENA_EDEN3S, (0, 0), 0, 2, 2)
        spriteList.append(self.drawable)
