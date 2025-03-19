import sys

from combat_card import CombatCard
from phase import Phase


class DrawPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        # TODO: if an unplayable drill is drawn, it can be shuffled back into the deck
        for _ in range(3):
            card = self.player.draw()
