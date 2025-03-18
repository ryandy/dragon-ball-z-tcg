import random
import sys

from phase import Phase


class DiscardPhase(Phase):
    def __init__(self, player, combat_phase):
        self.player = player
        self.combat_phase = combat_phase

    def execute(self):
        # TODO player choice
        while len(self.player.hand) > 1:
            idx = random.randrange(len(self.player.hand))
            self.player.discard(idx)

        # TODO player choice
        while len(self.player.opponent.hand) > 1:
            idx = random.randrange(len(self.player.opponent.hand))
            self.player.opponent.discard(idx)

        if self.combat_phase.skipped:
            self.player.rejuvenate()
