import arcade
from ..NPC import NPC
from ..Drawable import TextDrawable, CastBar, Circle, ThickLine, SpriteDrawable, Drawable
from ..Events import CallbackEvent, GotoEvent, KnockbackEvent
from ..helper import Vector, MOVEMENT_SPEED
from .. import AssetPath


class Duty():
    def __init__(self, gameWindow):
        self.gw = gameWindow
        self.eq = gameWindow.eventQueue
        self.party = gameWindow.party
        self.boss = None
        self.markers = {}
        self.assignedSpots = {}

    def makeBoss(self, icon, center, angle, size, hitsize):
        self.boss = NPC(icon, center, size, hitsize, 3, self.gw.sprites)
        self.boss.angle = angle
        self.gw.sprites.append(self.boss)

    def getColor(self, color):
        if not hasattr(arcade.color, color):
            print(f'{color} is not a valid color name')
            return arcade.color.WHITE
        return getattr(arcade.color, color)

    def getTarget(self, target):
        if isinstance(target, (Vector, tuple, list, Drawable)):
            return target
        if isinstance(target, str):
            if target[-1] in ['0', '1']:
                return self.party.get(target[:-1], int(target[-1]))
            if target == 'boss':
                return self.boss
        assert(False, f'unknown target {target}')

    def countdown(self, value):
        for i in range(value+1):
            text = f'{value-i}'
            if i == value:
                text = 'START!'
            td = TextDrawable(text, (0, 0), arcade.color.BANANA_YELLOW, 64, 4)
            self.eq.addDrawableEvent(self.gw, i+1, td, 1)

    def placeMarkers(self, markers):
        self.markers = markers
        for marker, pos in markers.items():
            icon = getattr(AssetPath, 'MARKER_'+marker)
            markerSprite = SpriteDrawable(icon, pos, 1.2, 0.15, 0.15)
            self.gw.sprites.append(markerSprite)

    def callback(self, when, what):
        self.eq.addEvent(CallbackEvent(self.gw, when, what))

    def goto(self, when, who, where, angle, scatter=0.1, speed=MOVEMENT_SPEED):
        if isinstance(where, str):
            where = self.markers[where]
        if who == 'all':
            self.eq.addEvent(GotoEvent(self.gw, when, self.party, where, angle, scatter, speed))
            return
        player = self.getTarget(who)
        self.eq.addEvent(GotoEvent(self.gw, when, player, where, angle, 0.0, speed))

    def gotoSpots(self, when, mechanic, speed=MOVEMENT_SPEED):
        spots = self.assignedSpots[mechanic]
        for who, where in spots.items():
            m = self.getTarget(who)
            self.goto(when, m, where, 0, 0, speed)

    def knockback(self, when, angle, distance):
        self.eq.addEvent(KnockbackEvent(self.gw, when, angle, distance))

    def castBar(self, when, howLong, what):
        cast = CastBar(howLong, what)
        self.eq.addDrawableEvent(self.gw, when, cast, howLong)

    def circle(self, when, howLong, where, howBig, color, layer=1, snapshot=False):
        target = self.getTarget(where)
        effect = Circle(target, howBig, self.getColor(color), layer, snapshot)
        self.eq.addDrawableEvent(self.gw, when, effect, howLong)
        return effect

    def thickLine(self, when, howLong, start, end, thickness, length, color, layer, snapshot=False):
        target1 = self.getTarget(start)
        target2 = self.getTarget(end)
        effect = ThickLine(target1, target2, thickness, self.getColor(color), length, layer, snapshot)
        self.eq.addDrawableEvent(self.gw, when, effect, howLong)
