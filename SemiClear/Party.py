import random
from .Drawable import Drawable
from .Player import Player
from .NPC import NPC
from . import AssetPath
from .helper import Vector


class Party(Drawable):
    def __init__(self, playerRole):
        super().__init__()
        self.roles = {'tank': 2, 'healer': 2, 'ranged': 2, 'melee': 2}
        self.roles[playerRole] -= 1
        self.player = Player(self.getAsset(playerRole), (0, 0), 1.0)
        self.members = []
        for role, num in self.roles.items():
            for _ in range(num):
                npc = NPC(self.getAsset(role), (0, 0), 1.0)
                self.members.append(npc)
        self.members.append(self.player)
        self.setPosition(Vector(0, -0.8), 0.2)

    def getAsset(self, role):
        return getattr(AssetPath, role.upper())

    def update(self, dt):
        for m in self.members:
            m.update(dt)

    def draw(self):
        for m in self.members:
            m.draw()

    def setPosition(self, center, radius):
        for m in self.members:
            rx = (random.random() * 2 - 1) * radius
            ry = (random.random() * 2 - 1) * radius
            m.pos = center + Vector(rx, ry)
