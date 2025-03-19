import sys

from phase import Phase


class NonCombatPhase(Phase):
    def __init__(self, player):
        self.player = player

    def execute(self):
        # TODO: Choice
        while self.player.play_non_combat_card():
            pass
