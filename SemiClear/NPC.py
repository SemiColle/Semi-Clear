import arcade
from .helper import coordsToPix, Vector, sizeToPix
from .Drawable import Drawable
from . import AssetPath

class NPC(Drawable):
    MODE_STOP = 'stop'
    MODE_GOTO = 'goto'
    MODE_PLAYER = 'play'

    def __init__(self, icon, center, size, hitsize, layer=2):
        super().__init__(layer, center)
        pixSize, pixHitsize = sizeToPix(size), sizeToPix(hitsize)
        self.sprite = arcade.Sprite(icon)
        self.sprite.width, self.sprite.height = pixSize, pixSize
        self.hitbox = arcade.Sprite(AssetPath.HITBOX)
        self.hitbox.width, self.hitbox.height = pixHitsize, pixHitsize
        self.movMode = NPC.MODE_STOP
        self.angle = 0
        self.targetPos = Vector(0, 0)
        self.targetAngle = 0
        self.speed = 0.5

    def draw(self):
        self.hitbox.draw()
        self.sprite.draw()

    def update(self, dt):
        pixPos = coordsToPix(self.center)
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        self.sprite.center_x = pixPos.x
        self.sprite.center_y = pixPos.y
        self.hitbox.center_x = pixPos.x
        self.hitbox.center_y = pixPos.y
        self.hitbox.angle = self.angle
        if self.movMode == NPC.MODE_GOTO:
            self.moveSpriteGoto(dt)

    def goto(self, targetPos, targetAngle, speed):
        self.targetPos = Vector(targetPos)
        self.targetAngle = targetAngle
        self.speed = speed
        self.movMode = NPC.MODE_GOTO

    def moveSpriteGoto(self, dt):
        vector = self.targetPos - self.center
        length = vector.length()
        if length < 0.01:
            self.movMode = NPC.MODE_STOP
            return
        if length >= self.speed*dt:
            vector = vector.normalize(self.speed*dt)
        self.center = self.center + vector
