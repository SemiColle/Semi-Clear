import arcade
from .helper import coordsToPix, Vector, sizeToPix, randomVector, MOVEMENT_SPEED
from .Drawable import SpriteDrawable, Drawable
from . import AssetPath


class NPC(Drawable):
    MODE_STOP = 'stop'
    MODE_GOTO = 'goto'
    MODE_PLAYER = 'play'

    def __init__(self, icon, center, size, hitsize, layer, spriteList):
        super().__init__(0, center)
        self.drawable = SpriteDrawable(icon, self, layer, size, size)
        self.hitbox = SpriteDrawable(AssetPath.HITBOX, self, 1, hitsize, hitsize)
        spriteList.append(self.drawable)
        spriteList.append(self.hitbox)

        self.movMode = NPC.MODE_STOP
        self.angle = 0
        self.targetPos = Vector(0, 0)
        self.targetAngle = 0
        self.speed = MOVEMENT_SPEED

    def update(self, dt):
        super().update(dt)
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        self.hitbox.sprite.angle = self.angle
        if self.movMode == NPC.MODE_GOTO:
            self.moveSpriteGoto(dt)

    def goto(self, targetPos, targetAngle, scatter, speed=MOVEMENT_SPEED, knockback=False):
        if self.isPlayer() and not knockback:
            return
        self.targetPos = Vector(targetPos)
        if scatter > 0:
            self.targetPos = self.targetPos + randomVector(scatter)
        self.targetAngle = targetAngle
        self.speed = speed
        self.movMode = NPC.MODE_GOTO

    def moveSpriteGoto(self, dt):
        vector = self.targetPos - self.center
        length = vector.length()
        if length < 0.01:
            if self.isPlayer():
                self.movMode = NPC.MODE_PLAYER
                self.speed = MOVEMENT_SPEED
            else:
                self.movMode = NPC.MODE_STOP
            return
        if length >= self.speed*dt:
            vector = vector.normalize(self.speed*dt)
        self.center = self.center + vector

    def isPlayer(self):
        return False
