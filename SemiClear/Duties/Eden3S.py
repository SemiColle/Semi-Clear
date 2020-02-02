import arcade
from ..Arena import Eden3SArena
from ..NPC import NPC
from ..Drawable import TextDrawable, CastBar, Circle, ThickLine
from ..Events import CallbackEvent, GotoEvent
from ..helper import MOVEMENT_SPEED
from .. import AssetPath


class Eden3S():
    def __init__(self, gameWindow):
        self.gw = gameWindow
        self.eq = gameWindow.eventQueue
        self.party = gameWindow.party
        self.arena = Eden3SArena(gameWindow.sprites)
        self.boss = NPC(AssetPath.BOSS_LEVIATHAN, (0, 1), 0.8, 2, 3, gameWindow.sprites)
        self.boss.angle = 180
        gameWindow.sprites.append(self.boss)
        self.addMechanics()

    def addMechanics(self):
        self.countdown(3)

    def countdown(self, value):
        for i in range(value+1):
            text = f'{value-i}'
            if i == value:
                text = 'START!'
            td = TextDrawable(text, (0, 0), arcade.color.BANANA_YELLOW, 64, 4)
            self.eq.addDrawableEvent(self.gw, i+1, td, 1)
        self.eq.addEvent(CallbackEvent(self.gw, value+1, self.firstPhase))

    def firstPhase(self):
        self.eq.addEvent(GotoEvent(self.gw, 0, self.party, (0, 0.1), 0, 0.1, MOVEMENT_SPEED))
        self.tidalRoar(6)
        self.ripCurrent(15)

    def tidalRoar(self, start):
        castTime = 4
        trCast = CastBar(castTime, 'Tidal Roar')
        self.eq.addDrawableEvent(self.gw, start, trCast, castTime)
        trEffect = Circle((0, 0), 5, arcade.color.LIGHT_BLUE, 1.1)
        self.eq.addDrawableEvent(self.gw, start+castTime, trEffect, 1)

    def ripCurrent(self, start):
        castTime = 4
        rcCast = CastBar(castTime, 'Rip Current')
        self.eq.addEvent(GotoEvent(self.gw, start+1, self.party.get('tank', 0), (-0.5, 0.1), 0, 0.1, MOVEMENT_SPEED))
        self.eq.addEvent(GotoEvent(self.gw, start+1, self.party.get('tank', 1), (0.5, 0.1), 0, 0.1, MOVEMENT_SPEED))
        self.eq.addDrawableEvent(self.gw, start, rcCast, castTime)
        rcEffect1 = ThickLine(self.boss, self.party.get('tank', 0), 0.3, arcade.color.LIGHT_BLUE, 5, 1, True)
        self.eq.addDrawableEvent(self.gw, start+castTime, rcEffect1, 1)
        rcEffect2 = ThickLine(self.boss, self.party.get('tank', 1), 0.3, arcade.color.LIGHT_BLUE, 5, 1, True)
        self.eq.addDrawableEvent(self.gw, start+castTime+2, rcEffect2, 1)
