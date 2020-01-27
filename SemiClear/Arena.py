import arcade
from .Drawable import Drawable
from . import helper


class Arena(Drawable):
    def __init__(self):
        super().__init__()

    def draw(self):
        arcade.draw_rectangle_filled(helper.ARENA_CENTER_X, helper.ARENA_CENTER_Y,
            helper.ARENA_WIDTH, helper.ARENA_HEIGHT, arcade.color.CAMEL)

    def update(self, dt):
        pass
