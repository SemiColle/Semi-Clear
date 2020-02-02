import arcade, random
from ..Arena import Eden3SArena
from ..NPC import NPC
from ..Drawable import TextDrawable, Circle, ThickLine
from ..Events import CallbackEvent
from ..helper import MOVEMENT_SPEED
from .. import AssetPath
from .Duty import Duty


class Eden3S(Duty):
    def __init__(self, gameWindow):
        super().__init__(gameWindow)
        self.arena = Eden3SArena(gameWindow)
        self.makeBoss(AssetPath.BOSS_LEVIATHAN, (0, 1), 180, 0.8, 2)
        self.placeMarkers({'A': (-0.45, 0.9), 'B': (0.45, 0.9), 'C': (0.45, -0.9), 'D':(-0.45, -0.9), '1': (-0.45, 0), '2': (0.45, 0)})
        self.assignedSpots = {'Freak Wave': {
            'tank0': (-0.45, 0.6), 'melee0': (-0.45, 0.2), 'healer0': (-0.45, -0.2), 'ranged0': (-0.45, -0.6),
            'tank1': ( 0.45, 0.6), 'melee1': ( 0.45, 0.2), 'healer1': ( 0.45, -0.2), 'ranged1': ( 0.45, -0.6)}}
        self.addMechanics()

    def addMechanics(self):
        self.countdown(3)
        self.firstPhase(4)

    def firstPhase(self, start):
        self.goto(start, 'all', (0, 0.1), 0)
        self.tidalRoar(start+9)
        self.ripCurrent(start+19)
        self.tidalWave(start+33)
        self.temporaryCurrent(start+46)
        self.drenchingPulse(start+58)
        self.temporaryCurrent(start+67)
        self.goto(start+78, 'all', (0, 0.1), 0)
        self.callback(start+80, self.arena.restore)

    def tidalRoar(self, start):
        castTime = 4
        self.castBar(start, castTime, 'Tidal Roar')
        self.circle(start+castTime, 1, (0, 0), 5, 'LIGHT_BLUE', 1.1)

    def ripCurrent(self, start):
        castTime = 5
        self.castBar(start, castTime, 'Rip Current')
        self.goto(start+1, 'tank0', (-0.5, 0.1), angle=0)
        self.goto(start+1, 'tank1', (0.5, 0.1), angle=0)
        self.thickLine(start+castTime, 1, 'boss', 'tank0', 0.3, 5, 'LIGHT_BLUE', 1, True)
        self.thickLine(start+castTime+1, 1, 'boss', 'tank1', 0.3, 5, 'LIGHT_BLUE', 1, True)

    def tidalWave(self, start):
        opt = random.choice([[(-1.1, 0), -90, 'A'], [(1.1, 0), 90, 'B']])
        self.castBar(start, 4, 'Tidal Wave')
        self.circle(start+4, 10, opt[0], 0.1, 'LIGHT_BLUE')
        self.castBar(start+5, 6, 'Undersea Quake')
        self.goto(start+5, 'all', opt[2], 0, 0.03)
        self.callback(start+11, self.arena.breakSides)
        self.knockback(start+14, opt[1], 0.9)

    def temporaryCurrent(self, start):
        opt = random.choice([[(1, 1), 'A'], [(-1, 1), 'B']])
        self.goto(start, 'boss', opt[0], -180, 0, 2)
        self.castBar(start, 6, 'Temporary Current')
        self.goto(start+3, 'all', opt[1], 0, 0.03)
        self.thickLine(start+6, 2, opt[0], (0, 0), 1.5, 5, 'LIGHT_BLUE', 1)
        self.goto(start+8, 'boss', (0, 1), -180, 0, 2)

    def drenchingPulse(self, start):
        self.goto(start-2, 'all', (0, 0.1), 0, 0.05)
        self.castBar(start, 3, 'Drenching Pulse')
        self.gotoSpots(start+4, 'Freak Wave')
        for m in self.party.members:
            c = self.circle(start+3, 2, m.drawable, 0.4, 'TIGERS_EYE', 1, True)
            self.circle(start+6, 1, c, 0.4, 'LIGHT_BLUE', 1, True)
            self.circle(start+5, 6, m.drawable, 0.25, 'TIGERS_EYE', 1.1)
            self.circle(start+11, 1, m.drawable, 0.25, 'LIGHT_BLUE', 1.1, True)
