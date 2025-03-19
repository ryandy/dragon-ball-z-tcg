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
            self.player.discard(random.choice(self.player.hand.cards))

        # TODO player choice
        while len(self.player.opponent.hand) > 1:
            self.player.opponent.discard(random.choice(self.player.opponent.hand.cards))

        if self.combat_phase.skipped:
            self.player.rejuvenate()
