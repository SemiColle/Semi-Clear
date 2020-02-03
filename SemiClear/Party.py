from .Drawable import Drawable
from .Player import Player
from .NPC import NPC
from . import AssetPath
from .helper import Vector, randomVector, rotateVector, PLAYER_SIZE, MOVEMENT_SPEED


class Party():
    def __init__(self, playerRole, spriteList):
        self.roles = {'tank': 2, 'healer': 2, 'ranged': 2, 'melee': 2}
        self.roles[playerRole] -= 1
        self.player = Player(self.getAsset(playerRole), (0, 0), PLAYER_SIZE, PLAYER_SIZE*1.5, 2.0, spriteList)
        spriteList.append(self.player)
        self.members = []
        for role, num in self.roles.items():
            setattr(self, role, [])
            for _ in range(num):
                npc = NPC(self.getAsset(role), (0, 0), PLAYER_SIZE, PLAYER_SIZE*1.5, 1.9, spriteList)
                spriteList.append(npc)
                self.members.append(npc)
                getattr(self, role).append(npc)
        self.members.append(self.player)
        getattr(self, playerRole).append(self.player)
        self.setPosition(Vector(0, -0.8), 0.1)

    def getAsset(self, role):
        return getattr(AssetPath, role.upper())

    def get(self, role=None, index=None):
        if role is None: # get all
            return self.get('tank') + self.get('healer') + self.get('ranged') + self.get('melee')
        if index is None: # get all from one role
            return getattr(self, role)
        return getattr(self, role)[index] # get one member

    def update(self, dt):
        for m in self.members:
            m.update(dt)

    def draw(self):
        for m in self.members:
            m.draw()

    def setPosition(self, center, radius):
        for m in self.members:
            m.center = center + randomVector(radius)

    def knockback(self, angle, distance, speed=1.0):
        for m in self.members:
            direction = rotateVector(Vector(0, distance), angle)
            targetPos = m.center + direction
            m.goto(targetPos, m.angle, 0, 1.0, True)
