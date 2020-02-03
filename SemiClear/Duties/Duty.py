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
        if isinstance(target, (Vector, tuple, Drawable, str)):
            target = [target]
        result = []
        if isinstance(target, list):
            for t in target:
                if isinstance(t, (Vector, tuple, Drawable)):
                    result.append(t)
                elif t == 'all':
                    result += self.party.get()
                elif t == 'boss':
                    result.append(self.boss)
                elif t[-1] == 's':
                    result += self.party.get(t[:-1])
                elif t[-1] in ['0', '1']:
                    result.append(self.party.get(t[:-1], int(t[-1])))
        if len(result) == 0:
            print(f'unknown target {target}')
        return result

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

    def goto(self, when, who, where, angle, scatter=0, speed=MOVEMENT_SPEED):
        if isinstance(where, str):
            where = self.markers[where]
        players = self.getTarget(who)
        for p in players:
            self.eq.addEvent(GotoEvent(self.gw, when, p, where, angle, scatter, speed))

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
        targets = self.getTarget(where)
        effects = []
        for t in targets:
            effect = Circle(t, howBig, self.getColor(color), layer, snapshot)
            self.eq.addDrawableEvent(self.gw, when, effect, howLong)
            effects.append(effect)
        return effects

    def thickLine(self, when, howLong, start, end, thickness, length, color, layer, snapshot=False):
        target1 = self.getTarget(start)
        target2 = self.getTarget(end)
        assert(len(target1) == 1, 'thick lines can only originate from a single target')
        for t in target2:
            effect = ThickLine(target1[0], t, thickness, self.getColor(color), length, layer, snapshot)
            self.eq.addDrawableEvent(self.gw, when, effect, howLong)
