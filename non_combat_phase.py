import sys

from phase import Phase


class NonCombatPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        pass
