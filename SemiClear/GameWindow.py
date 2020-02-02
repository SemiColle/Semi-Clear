import arcade
from operator import attrgetter

from .Party import Party
from .Duties import TestBoss, Eden3S
from .Events import EventQueue, DrawableEvent
from .Drawable import Circle, CastBar
from . import helper


class GameWindow(arcade.Window):
    def __init__(self, title):
        super().__init__(helper.WINDOW_WIDTH, helper.WINDOW_HEIGHT, title)

        arcade.set_background_color(arcade.color.BLACK)
        self.sprites = []
        self.party = Party('healer', self.sprites)
        self.mechanicHits = 0
        self.eventQueue = EventQueue()
        self.duty = Eden3S(self)
        self.gameSpeed = 1

    def on_update(self, dt):
        dt = dt * self.gameSpeed
        self.eventQueue.update(dt)
        for s in self.sprites:
            s.update(dt)
        self.sprites = [x for x in self.sprites if x.active]

    def on_draw(self):
        arcade.start_render()
        self.sprites.sort(key=attrgetter('layer'))
        for s in self.sprites:
            s.draw()
        statusPos = helper.coordsToPix(helper.Vector(1.3, 0.1))
        arcade.draw_text(f'mechanic hits: {self.mechanicHits}', statusPos.x, statusPos.y, arcade.color.WHITE, helper.FONT_SIZE, anchor_x='center')

    def on_key_press(self, key, keyModifiers):
        self.party.player.on_key_press(key, keyModifiers)
        if hasattr(self.duty, 'on_key_press'):
            self.duty.on_key_press(key, keyModifiers)

    def on_key_release(self, key, keyModifiers):
        self.party.player.on_key_release(key, keyModifiers)
