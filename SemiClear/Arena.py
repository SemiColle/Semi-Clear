import arcade
from .Drawable import Drawable
from . import helper


class Arena(Drawable):
    def __init__(self):
        super().__init__(0, helper.Vector(0, 0))

    def draw(self):
        pixPos = helper.coordsToPix(self.center)
        arcade.draw_rectangle_filled(pixPos.x, pixPos.y,
            helper.ARENA_WIDTH, helper.ARENA_HEIGHT, arcade.color.CAMEL)
