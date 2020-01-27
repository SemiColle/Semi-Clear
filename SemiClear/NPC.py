import arcade
from .helper import coordsToPix, Vector
from .Drawable import Drawable


class NPC(Drawable):
    MODE_STOP = 'stop'
    MODE_GOTO = 'goto'
    MODE_PLAYER = 'play'

    def __init__(self, icon, pos, scale):
        super().__init__()
        self.sprite = arcade.Sprite(icon, scale=scale)
        self.movMode = NPC.MODE_STOP
        self.pos = Vector(pos)
        self.angle = 0
        self.targetPos = Vector(0, 0)
        self.targetAngle = 0
        self.speed = 0.5

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        pixPos = coordsToPix(self.pos)
        self.sprite.center_x = pixPos.x
        self.sprite.center_y = pixPos.y
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        self.sprite.angle = self.angle
        if self.movMode == NPC.MODE_GOTO:
            self.moveSpriteGoto(dt)

    def goto(self, targetPos, targetAngle, speed):
        self.targetPos = Vector(targetPos)
        self.targetAngle = targetAngle
        self.speed = speed
        self.movMode = NPC.MODE_GOTO

    def moveSpriteGoto(self, dt):
        vector = self.targetPos - self.pos
        length = vector.length()
        if length < 0.01:
            self.movMode = NPC.MODE_STOP
            return
        if length >= self.speed*dt:
            vector = vector.normalize(self.speed*dt)
        self.pos = self.pos + vector
