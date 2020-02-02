import arcade
from ..Arena import TestArena
from ..NPC import NPC
from .. import AssetPath
from ..Drawable import CastBar, Circle, Donut, ThickLine, AngledLine, Cone, SpriteDrawable
from ..helper import Vector, rotateVector, PLAYER_SIZE
from .Duty import Duty


class TestBoss(Duty):
    def __init__(self, gameWindow):
        super().__init__(gameWindow)
        self.arena = TestArena(gameWindow)
        self.boss = NPC(AssetPath.BOSS_TITANIA, (0, 0), 0.5, 0.4, 3, gameWindow.sprites)
        gameWindow.sprites.append(self.boss)

        gameWindow.sprites.append(SpriteDrawable(AssetPath.SWIRLING_WATERS, self.party.player, 2.1, PLAYER_SIZE*0.8, PLAYER_SIZE*0.8, Vector(-0.04, 0.04)))
        gameWindow.sprites.append(SpriteDrawable(AssetPath.SPLASHING_WATERS, Vector(0.5, 1.1), 2, PLAYER_SIZE*0.8, PLAYER_SIZE*0.8))
        gameWindow.sprites.append(AngledLine((1, 1), -45, 0.2, 0.05, arcade.color.BANANA_MANIA))

    def on_key_press(self, key, keyModifiers):
        if key == arcade.key.KEY_1:
            self.boss.goto((-0.5, 0.5), 270, 2)
        if key == arcade.key.KEY_2:
            self.boss.goto((0.5, 0.5), 90, 2)
        if key == arcade.key.KEY_5:
            self.addCastedCircle((0, 0.3), 0.5, 0, 4)
        if key == arcade.key.KEY_6:
            self.addCastedDonut(0, 3)
        if key == arcade.key.KEY_7:
            self.addCastedCone(3)
        if key == arcade.key.KEY_8:
            self.party.knockback(self.party.player.angle, 0.5)

    def addCastedCircle(self, pos, radius, startTime, castTime):
        castBar = CastBar(castTime, 'Butt Spank')
        circleMarker = Circle(pos, radius, arcade.color.TIGERS_EYE)
        circle = Circle(pos, radius, arcade.color.WHITE)
        self.eq.addDrawableEvent(self.gw, startTime, castBar, castTime)
        self.eq.addDrawableEvent(self.gw, startTime, circleMarker, castTime)
        self.eq.addDrawableEvent(self.gw, startTime+castTime, circle, 1)

    def addCastedDonut(self, startTime, castTime):
        castBar = CastBar(castTime, 'Tasty Donut')
        donutMarker = Donut(self.party.player, 0.2, 0.6, arcade.color.TIGERS_EYE)
        donut = Donut(self.party.player, 0.2, 0.6, arcade.color.WHITE, snapshot=True)
        self.eq.addDrawableEvent(self.gw, startTime, castBar, castTime)
        self.eq.addDrawableEvent(self.gw, startTime, donutMarker, castTime)
        self.eq.addDrawableEvent(self.gw, startTime+castTime, donut, 1)

    def addCastedCone(self, castTime):
        castBar = CastBar(castTime, 'Pizza Slice')
        tether = ThickLine(self.boss, self.party.player, 0.03, arcade.color.STEEL_BLUE)
        cone = Cone(self.boss, self.party.player, 45, arcade.color.BITTERSWEET_SHIMMER, 5, snapshot=True)
        self.eq.addDrawableEvent(self.gw, 0, castBar, castTime)
        self.eq.addDrawableEvent(self.gw, 0, tether, castTime)
        self.eq.addDrawableEvent(self.gw, castTime, cone, 2)
