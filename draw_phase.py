import sys

from combat_card import CombatCard
from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        for _ in range(3):
            card = self.player.draw()
