import arcade
from .NPC import NPC


class Player(NPC):
    def __init__(self, icon, pos, scale):
        super().__init__(icon, pos, scale)
        self.keyMap = {
            arcade.key.W: 'up', arcade.key.S: 'down',
            arcade.key.A: 'left', arcade.key.D: 'right',
            arcade.key.Q: 'turnL', arcade.key.E: 'turnR'
        }
        self.keyPressed = {
            'up': False, 'down': False,
            'left': False, 'right': False,
            'turnL': False, 'turnR': False
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
        self.pos.x += dt * self.speed * (self.keyPressed['right'] - self.keyPressed['left'])
        self.pos.y += dt * self.speed * (self.keyPressed['up'] - self.keyPressed['down'])
        self.angle += dt * 100 * (self.keyPressed['turnL'] - self.keyPressed['turnR'])
