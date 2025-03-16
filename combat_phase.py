import sys

from phase import Phase


class CombatPhase(Phase):
    def __init__(self, player):
        self.player = player
        self.passed = True

    def execute(self):
        pass
