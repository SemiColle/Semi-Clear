import arcade
from ..Arena import Arena
from ..NPC import NPC
from .. import AssetPath
from ..Drawable import CastBar, Circle, Debuff, Donut, ThickLine, AngledLine, Cone
from ..helper import Vector, rotateVector


class TestBoss():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        self.arena = Arena()
        self.boss = NPC(AssetPath.TITANIA, (0, 0), 200, 150, layer=3)
        gameWindow.sprites.append(self.boss)
        gameWindow.sprites.append(self.arena)

        gameWindow.sprites.append(Debuff(AssetPath.SWIRLING_WATERS, gameWindow.party.player))
        gameWindow.sprites.append(Debuff(AssetPath.SPLASHING_WATERS, Vector(0.5, 1.1)))
        gameWindow.sprites.append(AngledLine((1, 1), -45, 0.2, 20, arcade.color.BANANA_MANIA))

    def on_key_press(self, key, keyModifiers):
        if key == arcade.key.KEY_5:
            self.addCastedCircle((0, 0.3), 200, 0, 4)
        if key == arcade.key.KEY_6:
            self.addCastedDonut(0, 3)
        if key == arcade.key.KEY_7:
            self.addCastedCone(3)

    def addMechanics(self):
        pass

    def addCastedCircle(self, pos, radius, startTime, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Butt Spank')
        circleMarker = Circle(pos, radius, arcade.color.TIGERS_EYE)
        circle = Circle(pos, radius, arcade.color.WHITE)
        eq.addDrawableEvent(gw, startTime, castBar, castTime)
        eq.addDrawableEvent(gw, startTime, circleMarker, castTime)
        eq.addDrawableEvent(gw, startTime+castTime, circle, 1)

    def addCastedDonut(self, startTime, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Tasty Donut')
        donutMarker = Donut(gw.party.player, 50, 150, arcade.color.TIGERS_EYE)
        # TODO: donut flashes in wrong position and then follows moving player
        donut = Donut(gw.party.player, 55, 150, arcade.color.WHITE)
        eq.addDrawableEvent(gw, startTime, castBar, castTime)
        eq.addDrawableEvent(gw, startTime, donutMarker, castTime)
        eq.addDrawableEvent(gw, startTime+castTime, donut, 1)

    def addCastedCone(self, castTime):
        eq = self.gameWindow.eventQueue
        gw = self.gameWindow
        castBar = CastBar(castTime, 'Pizza Slice')
        # TODO: fix crash
        # tether = ThickLine(self.boss, gw.party.player, 10, arcade.color.STEEL_BLUE)
        # TODO: use position of player WHEN CONE TRIGGERS
        cone = Cone((0, 0), gw.party.player.center, 45, arcade.color.BITTERSWEET_SHIMMER, 5)
        eq.addDrawableEvent(gw, 0, castBar, castTime)
        # eq.addDrawableEvent(gw, 0, tether, castTime)
        eq.addDrawableEvent(gw, castTime, cone, 2)
