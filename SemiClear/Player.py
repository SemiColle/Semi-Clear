import arcade, math
from .NPC import NPC


class Player(NPC):
    def __init__(self, icon, center, size, hitsize):
        super().__init__(icon, center, size, hitsize)
        self.keyMap = {
            arcade.key.W: 'up', arcade.key.S: 'down',
            arcade.key.A: 'left', arcade.key.D: 'right'
        }
        self.keyPressed = {
            'up': False, 'down': False,
            'left': False, 'right': False
        }
        self.movMode = NPC.MODE_PLAYER

    def update(self, dt):
        if self.movMode == NPC.MODE_PLAYER:
            self.moveSpriteKey(dt)
        super().update(dt)

    def on_key_press(self, key, keyModifiers):
        if key in self.keyMap:
            mapped = self.keyMap[key]
            self.keyPressed[mapped] = True

    def on_key_release(self, key, keyModifiers):
        if key in self.keyMap:
            mapped = self.keyMap[key]
            self.keyPressed[mapped] = False

    def moveSpriteKey(self, dt):
        dx = dt * self.speed * (self.keyPressed['right'] - self.keyPressed['left'])
        dy = dt * self.speed * (self.keyPressed['up'] - self.keyPressed['down'])
        if not dx == 0 or not dy == 0:
            self.angle = math.degrees(math.atan2(-dx, dy))
        self.center.x += dx
        self.center.y += dy
