import arcade
from ..Arena import Arena
from ..NPC import NPC
from .. import AssetPath
from ..Drawable import CastBar, Circle


class TestBoss():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        self.arena = Arena()
        self.boss = NPC(AssetPath.TITANIA, (0, 0), 200, 150)
        gameWindow.sprites.append(self.boss)
        gameWindow.sprites.insert(0, self.arena)

    def addMechanics(self):
        self.addCastedCircle((0, 0.3), 50, 1, 2)
        self.addCastedCircle((-0.5, -0.3), 50, 5.2, 2)
        self.addCastedCircle((0, 0), 200, 10, 4)

    def addCastedCircle(self, pos, radius, startTime, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Butt Spank')
        eq.addDrawableEvent(gw, startTime, castBar, castTime)
        circle = Circle(pos, radius, arcade.color.RASPBERRY_PINK)
        eq.addDrawableEvent(gw, startTime+castTime, circle, 1)
