import arcade
from ..Arena import Eden3SArena
from ..NPC import NPC
from .. import AssetPath


class Eden3S():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        self.arena = Eden3SArena(gameWindow.sprites)
        self.boss = NPC(AssetPath.BOSS_LEVIATHAN, (0, 1), 0.8, 2, layer=3)
        self.boss.angle = 180
        gameWindow.sprites.append(self.boss)
