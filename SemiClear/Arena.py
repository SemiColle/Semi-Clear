import arcade
from .Drawable import ThickLine, SpriteDrawable
from . import helper, AssetPath


class TestArena():
    def __init__(self, gameWindow):
        self.drawable = ThickLine((-1, 0), (1, 0), 2, arcade.color.CAMEL, None, 0)
        gameWindow.sprites.append(self.drawable)


class Eden3SArena():
    def __init__(self, gameWindow):
        self.gw = gameWindow
        self.drawable = SpriteDrawable(AssetPath.ARENA_EDEN3S, (0, 0), 0, 2, 2)
        self.left = ThickLine((-0.75, 1), (-0.75, -1), 0.5, arcade.color.BLACK, layer=0.001)
        self.right = ThickLine((0.75, 1), (0.75, -1), 0.5, arcade.color.BLACK, layer=0.001)
        self.center = ThickLine((0, 1), (0, -1), 1, arcade.color.BLACK, layer=0.001)
        self.gw.sprites.append(self.drawable)

    def breakSides(self):
        self.gw.sprites.append(self.left)
        self.gw.sprites.append(self.right)

    def breakCenter(self):
        self.gw.sprites.append(self.center)

    def restore(self):
        lst = self.gw.sprites
        if self.left in lst and self.right in lst:
            lst.remove(self.left)
            lst.remove(self.right)
        if self.center in lst:
            lst.remove(self.center)
