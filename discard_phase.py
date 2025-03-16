import random
import sys

from phase import Phase


class DiscardPhase(Phase):
    def __init__(self, player, combat_phase):
        self.player = player
        self.combat_phase = combat_phase

    def execute(self):
        while len(self.player.hand) > 1:
            idx = random.randrange(len(self.player.hand))
            self.player.discard(idx)

        if self.combat_phase.passed:
            self.player.rejuvenate()
        else:
            while len(self.player.opponent.hand) > 1:
                idx = random.randrange(len(self.player.opponent.hand))
                self.player.opponent.discard(idx)

        # "END OF TURN" (attacker before defender)
