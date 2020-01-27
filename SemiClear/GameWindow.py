import arcade

from .Party import Party
from .Duties.TestBoss import TestBoss
from .Events import EventQueue, DrawableEvent
from .Drawable import Circle, CastBar
from . import helper


class GameWindow(arcade.Window):
    def __init__(self, title):
        super().__init__(helper.WINDOW_WIDTH, helper.WINDOW_HEIGHT, title)

        arcade.set_background_color(arcade.color.BLACK)
        self.party = Party('ranged')
        self.sprites = [self.party]
        self.eventQueue = EventQueue()
        self.duty = TestBoss(self)
        self.duty.addMechanics()

    def on_update(self, dt):
        for s in self.sprites:
            s.update(dt)
        self.eventQueue.update(dt)
        self.sprites = [x for x in self.sprites if x.active]

    def on_draw(self):
        arcade.start_render()
        for s in self.sprites:
            s.draw()

    def on_key_press(self, key, keyModifiers):
        self.party.player.on_key_press(key, keyModifiers)
        if key == arcade.key.KEY_1:
            self.boss.goto((-0.5, 0.5), 270, 2)
        if key == arcade.key.KEY_2:
            self.boss.goto((0.5, 0.5), 90, 2)
        if key == arcade.key.KEY_3:
            circle = Circle((0.5, 0), 50, arcade.color.RASPBERRY_PINK)
            self.eventQueue.addDrawableEvent(self, 3, circle, 1, relative=True)
            castBar = CastBar(3, '', (0, 0.2), 100)
            self.eventQueue.addDrawableEvent(self, 0, castBar, 3, relative=True)

    def on_key_release(self, key, keyModifiers):
        self.party.player.on_key_release(key, keyModifiers)
