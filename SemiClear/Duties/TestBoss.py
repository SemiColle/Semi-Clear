import arcade
from ..Arena import Arena
from ..NPC import NPC
from .. import AssetPath
from ..Drawable import CastBar, Circle, Debuff, Donut
from ..helper import Vector


class TestBoss():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        self.arena = Arena()
        self.boss = NPC(AssetPath.TITANIA, (0, 0), 200, 150, layer=3)
        gameWindow.sprites.append(self.boss)
        gameWindow.sprites.append(self.arena)

        gameWindow.sprites.append(Debuff(AssetPath.SWIRLING_WATERS, gameWindow.party.player))
        gameWindow.sprites.append(Debuff(AssetPath.SPLASHING_WATERS, Vector(0.5, 1.1)))

    def on_key_press(self, key, keyModifiers):
        if key == arcade.key.KEY_5:
            self.addCastedCircle((0, 0.3), 200, 0, 4)
        if key == arcade.key.KEY_6:
            self.addCastedDonut(0, 3)

    def addMechanics(self):
        pass

    def addCastedCircle(self, pos, radius, startTime, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Butt Spank')
        circleMarker = Circle(pos, radius, arcade.color.TIGERS_EYE)
        circle = Circle(pos, radius, arcade.color.WHITE)
        eq.addDrawableEvent(gw, startTime, castBar, castTime, relative=True)
        eq.addDrawableEvent(gw, startTime, circleMarker, castTime, relative=True)
        eq.addDrawableEvent(gw, startTime+castTime, circle, 1, relative=True)

    def addCastedDonut(self, startTime, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Tasty Donut')
        donutMarker = Donut(gw.party.player, 50, 150, arcade.color.TIGERS_EYE)
        donut = Donut(gw.party.player, 55, 150, arcade.color.WHITE)
        eq.addDrawableEvent(gw, startTime, castBar, castTime, relative=True)
        eq.addDrawableEvent(gw, startTime, donutMarker, castTime, relative=True)
        eq.addDrawableEvent(gw, startTime+castTime, donut, 1, relative=True)
